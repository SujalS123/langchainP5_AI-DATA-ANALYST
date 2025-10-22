from ..llm.llm_client import LLMClient
from ..services.tools import PandasTool, prepare_bar_chart_data, prepare_line_chart_data, prepare_pie_chart_data
from ..services.query_parser import parse_chart_query, should_use_direct_parsing
import json
import pandas as pd
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.tools import Tool
import re

llm_client = LLMClient()
llm = llm_client._client

async def analyze_question(df: pd.DataFrame, question: str):
    # First try direct parsing for common chart patterns
    if should_use_direct_parsing(question):
        columns = list(df.columns)
        parsed_params = parse_chart_query(question, columns)
        
        if parsed_params:
            try:
                # Generate chart directly based on parsed parameters
                if parsed_params["chart_type"] == "bar":
                    chart_specification = prepare_bar_chart_data(
                        df,
                        x_col=parsed_params["x_col"],
                        y_col=parsed_params["y_col"],
                        n=parsed_params["n"],
                        title=parsed_params["title"]
                    )
                elif parsed_params["chart_type"] == "line":
                    chart_specification = prepare_line_chart_data(
                        df,
                        time_col=parsed_params["x_col"],
                        value_col=parsed_params["y_col"],
                        title=parsed_params["title"]
                    )
                elif parsed_params["chart_type"] == "pie":
                    chart_specification = prepare_pie_chart_data(
                        df,
                        label_col=parsed_params["x_col"],
                        value_col=parsed_params["y_col"],
                        n=parsed_params["n"],
                        title=parsed_params["title"]
                    )
                else:
                    chart_specification = None
                
                if chart_specification and not chart_specification.get("error"):
                    # Extract actual data from chart for detailed analysis
                    chart_data = chart_specification.get("data", {})
                    labels = chart_data.get("labels", [])
                    datasets = chart_data.get("datasets", [])
                    
                    detailed_analysis = ""
                    if labels and datasets:
                        dataset = datasets[0]
                        data_values = dataset.get("data", [])
                        y_label = dataset.get("label", "Value")
                        
                        if data_values and labels:
                            # Generate detailed analysis
                            detailed_analysis = f"\n\nDetailed Analysis:\n"
                            detailed_analysis += f"• Total items analyzed: {len(labels)}\n"
                            
                            if parsed_params["n"] and parsed_params["n"] < len(labels):
                                detailed_analysis += f"• Showing top {parsed_params['n']} items by {y_label.lower()}\n"
                            
                            # Top performers
                            if len(data_values) >= 3:
                                top_3 = list(zip(labels, data_values))[:3]
                                detailed_analysis += f"• Top 3 performers:\n"
                                for i, (label, value) in enumerate(top_3, 1):
                                    detailed_analysis += f"  {i}. {label}: {value:,.2f}\n"
                            
                            # Total and average
                            total_value = sum(data_values)
                            avg_value = total_value / len(data_values)
                            detailed_analysis += f"• Total {y_label.lower()}: {total_value:,.2f}\n"
                            detailed_analysis += f"• Average {y_label.lower()}: {avg_value:,.2f}\n"
                            
                            # Range
                            if len(data_values) > 1:
                                max_val = max(data_values)
                                min_val = min(data_values)
                                detailed_analysis += f"• Range: {min_val:,.2f} to {max_val:,.2f}\n"
                    
                    return {
                        "final_answer": f"I've generated a {parsed_params['chart_type']} chart showing {parsed_params['title'].lower()}.{detailed_analysis}",
                        "reasoning": "Used direct query parsing for efficient chart generation with detailed data analysis.",
                        "tool_results": [],
                        "chart_specification": chart_specification
                    }
            except Exception as e:
                print(f"Direct parsing failed: {e}, falling back to AI agent")
    
    # Fall back to AI agent for complex queries
    tool = PandasTool(df)

    # Add dataset_info tool for non-chart queries
    def get_dataset_info(query_type: str = "columns"):
        """Returns basic dataset information"""
        info = {}
        if "column" in query_type.lower() or not query_type.strip():
            info["columns"] = list(df.columns)
            info["count"] = len(df.columns)
        if "row" in query_type.lower() or "shape" in query_type.lower():
            info["rows"] = len(df)
        if "type" in query_type.lower() or "dtype" in query_type.lower():
            info["dtypes"] = df.dtypes.astype(str).to_dict()
        if not info:  # Default: return everything
            info = {
                "columns": list(df.columns),
                "column_count": len(df.columns),
                "row_count": len(df),
                "dtypes": df.dtypes.astype(str).to_dict()
            }
        return json.dumps(info, indent=2)

    # Helper function to safely parse JSON with extra quotes
    def safe_json_parse(input_str):
        """Parse JSON, handling extra quotes from LLM"""
        try:
            # Try direct parsing first
            return json.loads(input_str)
        except json.JSONDecodeError:
            # Strip outer quotes if present and try again
            if input_str.startswith("'") and input_str.endswith("'"):
                return json.loads(input_str[1:-1])
            elif input_str.startswith('"') and input_str.endswith('"'):
                return json.loads(input_str[1:-1])
            else:
                raise

    tools = [
        Tool(
            name="dataset_info",
            func=get_dataset_info,
            description="""Get dataset column names and structure. Use for: "what are the columns", "list columns", "column names", "dataset info".""",
        ),
        Tool(
            name="describe",
            func=lambda cols: tool.describe(safe_json_parse(cols)),
            description="""Get statistics for columns. Input: JSON list like ["col1"] or [] for all.""",
        ),
        Tool(
            name="top_n",
            func=lambda args: tool.top_n(
                by_col=safe_json_parse(args)["by_col"],
                n=int(safe_json_parse(args).get("n", 10)),
                ascending=safe_json_parse(args).get("ascending", False)
            ),
            description="""Get top N rows by column. Input: {"by_col": "Sales", "n": 10, "ascending": false}""",
        ),
        Tool(
            name="group_agg",
            func=lambda args: tool.group_agg(
                groupby_cols=safe_json_parse(args)["groupby"],
                agg_cols=safe_json_parse(args)["agg"]
            ),
            description="""Aggregate data by groups. Input: {"groupby": ["City"], "agg": {"Sales": "sum"}}""",
        ),
        Tool(
            name="correlation",
            func=lambda args: tool.correlation(
                col_x=safe_json_parse(args)["x"],
                col_y=safe_json_parse(args)["y"]
            ),
            description="""Get correlation between two columns. Input: {"x": "Sales", "y": "Profit"}""",
        ),
        Tool(
            name="filter",
            func=lambda expr: tool.filter(expr),
            description="""Filter rows. Input: Sales > 1000 and State == "CA" (no quotes around the expression)""",
        ),
        Tool(
            name="prepare_bar_chart",
            func=lambda args: prepare_bar_chart_data(
                df,
                x_col=safe_json_parse(args)["x"],
                y_col=safe_json_parse(args)["y"],
                n=int(safe_json_parse(args).get("n", 7)),
                title=safe_json_parse(args).get("title", None)
            ),
            description="""Create bar chart. ONLY for explicit visualization requests. Input: {"x": "State", "y": "Profit", "n": 5}""",
        ),
        Tool(
            name="prepare_line_chart",
            func=lambda args: prepare_line_chart_data(
                df,
                time_col=safe_json_parse(args)["time_col"],
                value_col=safe_json_parse(args)["value_col"],
                title=safe_json_parse(args).get("title", None)
            ),
            description="""Create line chart. ONLY for explicit visualization requests. Input: {"time_col": "Date", "value_col": "Sales"}""",
        ),
        Tool(
            name="prepare_pie_chart",
            func=lambda args: prepare_pie_chart_data(
                df,
                label_col=safe_json_parse(args)["label"],
                value_col=safe_json_parse(args)["value"],
                n=int(safe_json_parse(args).get("n", 7)),
                title=safe_json_parse(args).get("title", None)
            ),
            description="""Create pie chart. ONLY for explicit visualization requests. Input: {"label": "Category", "value": "Sales"}""",
        ),
    ]

    # MINIMAL PROMPT - Less is more!
    template = """Answer questions about a dataset with columns: {columns_list}

Tools: {tools}

RULES:
1. "What are the columns" → Use dataset_info
2. Statistics/analysis → Use describe, top_n, group_agg, correlation, filter
3. "Show me a chart/graph" → Use prepare_bar_chart, prepare_line_chart, prepare_pie_chart
4. Never create charts unless explicitly requested with words like "show", "visualize", "chart", "graph"

JSON FORMAT: For Action Input, use valid JSON WITHOUT extra quotes:
- CORRECT: ["Sales"]
- WRONG: '["Sales"]'
- CORRECT: {{"by_col": "Sales", "n": 10}}
- WRONG: '{{"by_col": "Sales", "n": 10}}'

ANSWER FORMAT: Provide detailed, well-formatted responses:
- Use bullet points for clarity
- Include relevant context and insights
- Format numbers with commas (e.g., 1,234.56)
- Highlight key findings
- Compare with other metrics when relevant (min, max, median)
- Use clear section headers

Example for "What is the average sales?":
Based on the analysis of 9,994 data points:

📊 Average Sales: $229.86

Key Statistics:
• Median Sales: $54.49 (half of sales are below this value)
• Minimum Sales: $0.44
• Maximum Sales: $22,638.48
• Standard Deviation: $623.25 (indicates high variability)

Insights:
• The average is significantly higher than the median, suggesting some very high-value sales are pulling the average up
• There's a wide range between minimum and maximum values
• 75% of sales are below $209.94

Format:
Question: the question
Thought: which tool to use and why
Action: tool name from [{tool_names}]
Action Input: valid JSON without outer quotes
Observation: tool output
... (repeat if needed)
Thought: I have the answer
Final Answer: [detailed, formatted answer with insights]

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)
    
    # Create the ReAct agent
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True,
        return_intermediate_steps=True,
        max_iterations=5  # Limit iterations to prevent runaway
    )

    columns = list(df.columns)
    
    def enhance_answer(final_answer: str, intermediate_steps: list) -> str:
        """Post-process answer to add more details and formatting"""
        
        # Check if answer is already detailed (has bullet points or multiple lines)
        if '•' in final_answer or '**' in final_answer or len(final_answer.split('\n')) > 3:
            return final_answer
        
        # Try to enhance based on tool outputs
        for action, observation in intermediate_steps:
            action_name = action.tool if hasattr(action, 'tool') else str(action)
            
            # Enhance dataset_info outputs
            if action_name == "dataset_info":
                try:
                    if isinstance(observation, str):
                        info = json.loads(observation)
                    else:
                        info = observation
                    
                    if "columns" in info:
                        columns = info["columns"]
                        enhanced = f"📊 **Dataset Overview**\n\n"
                        enhanced += f"This dataset contains **{len(columns)} columns** and **{info.get('row_count', len(df))} rows**.\n\n"
                        enhanced += f"**Available Columns:**\n"
                        
                        # Group columns by type if dtypes available
                        if "dtypes" in info:
                            dtypes = info["dtypes"]
                            numeric_cols = [col for col in columns if dtypes.get(col, "").startswith(("int", "float"))]
                            text_cols = [col for col in columns if dtypes.get(col, "") == "object"]
                            
                            if numeric_cols:
                                enhanced += f"\n**Numeric Columns** ({len(numeric_cols)}):\n"
                                for col in numeric_cols:
                                    enhanced += f"• {col}\n"
                            
                            if text_cols:
                                enhanced += f"\n**Text/Categorical Columns** ({len(text_cols)}):\n"
                                for col in text_cols:
                                    enhanced += f"• {col}\n"
                        else:
                            # Simple list if no type info
                            for i, col in enumerate(columns, 1):
                                enhanced += f"{i}. {col}\n"
                        
                        enhanced += f"\n💡 **Tip:** You can now ask questions like:\n"
                        enhanced += f"• 'What is the average Sales?'\n"
                        enhanced += f"• 'Show me top 10 States by Profit'\n"
                        enhanced += f"• 'Create a bar chart of Sales by Region'\n"
                        
                        return enhanced
                except (json.JSONDecodeError, KeyError):
                    pass
            
            # Enhance describe tool outputs
            if action_name == "describe" and isinstance(observation, dict):
                for col_name, stats in observation.items():
                    if isinstance(stats, dict):
                        count = stats.get('count', 0)
                        mean = stats.get('mean', 0)
                        median = stats.get('50%', 0)
                        std = stats.get('std', 0)
                        min_val = stats.get('min', 0)
                        max_val = stats.get('max', 0)
                        q25 = stats.get('25%', 0)
                        q75 = stats.get('75%', 0)
                        
                        # Create enhanced answer
                        enhanced = f"📊 **Analysis of {col_name}** (Based on {int(count):,} data points)\n\n"
                        enhanced += f"**Key Metrics:**\n"
                        enhanced += f"• Average: ${mean:,.2f}\n"
                        enhanced += f"• Median: ${median:,.2f}\n"
                        enhanced += f"• Range: ${min_val:,.2f} to ${max_val:,.2f}\n"
                        enhanced += f"• Standard Deviation: ${std:,.2f}\n\n"
                        enhanced += f"**Distribution:**\n"
                        enhanced += f"• 25th Percentile: ${q25:,.2f} (25% of values are below this)\n"
                        enhanced += f"• 50th Percentile (Median): ${median:,.2f}\n"
                        enhanced += f"• 75th Percentile: ${q75:,.2f} (75% of values are below this)\n\n"
                        
                        # Add insights
                        if mean > median * 1.5:
                            enhanced += f"**💡 Insight:** The average (${mean:,.2f}) is significantly higher than the median (${median:,.2f}), "
                            enhanced += f"indicating that some high-value outliers are pulling the average up. The median might be a better "
                            enhanced += f"representation of typical {col_name.lower()}.\n"
                        elif std > mean:
                            enhanced += f"**💡 Insight:** High variability detected (standard deviation > mean). "
                            enhanced += f"This suggests {col_name.lower()} values vary widely across the dataset.\n"
                        else:
                            enhanced += f"**💡 Insight:** The data shows moderate variability with most values "
                            enhanced += f"clustering around the average of ${mean:,.2f}.\n"
                        
                        return enhanced
            
            # Enhance top_n outputs
            elif action_name == "top_n" and isinstance(observation, list):
                if len(observation) > 0:
                    enhanced = f"📊 **Top {len(observation)} Results:**\n\n"
                    for i, item in enumerate(observation[:10], 1):
                        if isinstance(item, dict):
                            # Format each item nicely
                            enhanced += f"**{i}.** "
                            for key, value in item.items():
                                if isinstance(value, (int, float)):
                                    enhanced += f"{key}: ${value:,.2f}  "
                                else:
                                    enhanced += f"{key}: {value}  "
                            enhanced += "\n"
                    return enhanced
            
            # Enhance correlation outputs
            elif action_name == "correlation" and isinstance(observation, dict):
                corr_value = observation.get('correlation', 0)
                col_x = observation.get('col_x', 'X')
                col_y = observation.get('col_y', 'Y')
                
                enhanced = f"📊 **Correlation Analysis: {col_x} vs {col_y}**\n\n"
                enhanced += f"**Correlation Coefficient:** {corr_value:.4f}\n\n"
                enhanced += f"**Interpretation:**\n"
                
                if abs(corr_value) >= 0.7:
                    strength = "Strong"
                elif abs(corr_value) >= 0.4:
                    strength = "Moderate"
                else:
                    strength = "Weak"
                
                direction = "positive" if corr_value > 0 else "negative"
                
                enhanced += f"• {strength} {direction} correlation detected\n"
                
                if corr_value > 0:
                    enhanced += f"• As {col_x} increases, {col_y} tends to increase as well\n"
                else:
                    enhanced += f"• As {col_x} increases, {col_y} tends to decrease\n"
                
                if abs(corr_value) >= 0.7:
                    enhanced += f"• This indicates a strong relationship between the two variables\n"
                elif abs(corr_value) < 0.3:
                    enhanced += f"• The relationship between these variables is minimal\n"
                
                return enhanced
        
        return final_answer
    
    try:
        response = await agent_executor.ainvoke({
            "input": question,
            "columns_list": ", ".join(columns)
        })
        
        final_answer = response.get("output", "")
        chart_specification = None
        
        # If no final answer but we have intermediate steps, try to construct one
        if not final_answer and "intermediate_steps" in response and response["intermediate_steps"]:
            final_answer = "Analysis completed. See details below."
        
        # Enhance the answer with more details
        if "intermediate_steps" in response and response["intermediate_steps"]:
            enhanced_answer = enhance_answer(final_answer, response["intermediate_steps"])
            final_answer = enhanced_answer
        
        # IMPROVED: More precise chart extraction
        if "intermediate_steps" in response:
            for action, observation in response["intermediate_steps"]:
                # Only extract charts from chart preparation tools
                action_name = action.tool if hasattr(action, 'tool') else str(action)
                
                if action_name in ["prepare_bar_chart", "prepare_line_chart", "prepare_pie_chart"]:
                    if isinstance(observation, dict):
                        if observation.get('type') and observation.get('data'):
                            chart_specification = observation
                            break
                        elif observation.get('error'):
                            chart_specification = {"error": observation['error']}
                            break
                    elif isinstance(observation, str):
                        try:
                            # Parse JSON response
                            json_str = observation.replace("'", '"')
                            parsed = json.loads(json_str)
                            if parsed.get('type') and parsed.get('data'):
                                chart_specification = parsed
                                break
                        except json.JSONDecodeError:
                            # Try regex extraction
                            json_match = re.search(r'\{.*\}', observation, re.DOTALL)
                            if json_match:
                                try:
                                    json_str = json_match.group(0).replace("'", '"')
                                    parsed = json.loads(json_str)
                                    if parsed.get('type') and parsed.get('data'):
                                        chart_specification = parsed
                                        break
                                except json.JSONDecodeError:
                                    pass

        return {
            "final_answer": final_answer,
            "reasoning": "See agent execution log for detailed reasoning.",
            "tool_results": [],
            "chart_specification": chart_specification
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "error": f"Agent execution failed: {e}", 
            "raw": str(e), 
            "traceback": traceback.format_exc()
        }