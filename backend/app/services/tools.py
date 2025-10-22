import pandas as pd
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any

# PandasTool: wrapper functions to perform common operations
class PandasTool:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def list_columns(self):
        return list(self.df.columns)

    def head(self, n=5):
        return self.df.head(n).to_dict(orient="records")

    def describe(self, cols=None):
        if cols is None:
            desc = self.df.describe(include="all")
        else:
            desc = self.df[cols].describe()
        return desc.fillna("").to_dict()

    def group_agg(self, groupby_cols, agg_cols: Dict[str,str]):
        """
        groupby_cols: list or str
        agg_cols: {"revenue": "sum", "orders": "mean"}
        """
        res = self.df.groupby(groupby_cols).agg(agg_cols).reset_index()
        return res.to_dict(orient="records")

    def filter(self, expr:str):
        """
        expr: pandas query expression (we allow limited safe expressions)
        """
        safe_df = self.df.query(expr)
        return safe_df.to_dict(orient="records")
    
    def top_n(self, by_col, n=10, ascending=False):
        res = self.df.sort_values(by=by_col, ascending=ascending).head(n)
        return res.to_dict(orient="records")

    def correlation(self, col_x, col_y):
        if col_x not in self.df.columns or col_y not in self.df.columns:
            raise ValueError("missing columns")
        return float(self.df[col_x].corr(self.df[col_y]))

# Chart tool
def df_to_base64_png_plot(df, plot_fn):
    """
    df: pd.DataFrame
    plot_fn: function that takes (plt, df) and draws on plt
    returns: data:image/png;base64,...
    """
    plt.clf()
    plot_fn(plt, df)
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{b64}"

# Example plotting helpers (keeping for backward compatibility)
def plot_bar_top_n(plt, df, x_col, y_col, n=10, title=None):
    top = df.sort_values(by=y_col, ascending=False).head(n)
    plt.figure(figsize=(8,5))
    plt.bar(top[x_col].astype(str), top[y_col])
    plt.xticks(rotation=45, ha='right')
    if title: plt.title(title)

def plot_line_time(plt, df, time_col, value_col, title=None):
    df_sorted = df.sort_values(by=time_col)
    plt.figure(figsize=(8,5))
    plt.plot(df_sorted[time_col], df_sorted[value_col], marker='o')
    plt.xticks(rotation=45, ha='right')
    if title: plt.title(title)

# Chart data preparation functions for frontend rendering
def prepare_bar_chart_data(df, x_col, y_col, n=10, title=None):
    """
    Prepares bar chart data for frontend Chart.js rendering
    Returns structured JSON with chart specification
    """
    try:
        # Get top N values
        top_data = df.sort_values(by=y_col, ascending=False).head(n)
        
        # Prepare labels and data
        labels = top_data[x_col].astype(str).tolist()
        values = top_data[y_col].tolist()
        
        chart_spec = {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": str(y_col),
                    "data": values,
                    "backgroundColor": [
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 99, 132, 0.8)', 
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)',
                        'rgba(255, 159, 64, 0.8)',
                        'rgba(199, 199, 199, 0.8)',
                        'rgba(83, 102, 255, 0.8)',
                        'rgba(255, 99, 255, 0.8)',
                        'rgba(99, 255, 132, 0.8)'
                    ],
                    "borderColor": [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(199, 199, 199, 1)',
                        'rgba(83, 102, 255, 1)',
                        'rgba(255, 99, 255, 1)',
                        'rgba(99, 255, 132, 1)'
                    ],
                    "borderWidth": 1
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": title or f"Top {n} {x_col} by {y_col}"
                    },
                    "legend": {
                        "display": True,
                        "position": "top"
                    }
                },
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "title": {
                            "display": True,
                            "text": str(y_col)
                        }
                    },
                    "x": {
                        "title": {
                            "display": True,
                            "text": str(x_col)
                        }
                    }
                }
            }
        }
        
        return chart_spec
        
    except Exception as e:
        return {"error": f"Failed to prepare bar chart data: {str(e)}"}

def prepare_line_chart_data(df, time_col, value_col, title=None):
    """
    Prepares line chart data for frontend Chart.js rendering
    Returns structured JSON with chart specification
    """
    try:
        # Sort by time column
        sorted_data = df.sort_values(by=time_col)
        
        # Prepare labels and data
        labels = sorted_data[time_col].astype(str).tolist()
        values = sorted_data[value_col].tolist()
        
        chart_spec = {
            "type": "line",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": str(value_col),
                    "data": values,
                    "borderColor": 'rgba(54, 162, 235, 1)',
                    "backgroundColor": 'rgba(54, 162, 235, 0.2)',
                    "fill": True,
                    "tension": 0.1,
                    "pointBackgroundColor": 'rgba(54, 162, 235, 1)',
                    "pointBorderColor": '#fff',
                    "pointHoverBackgroundColor": '#fff',
                    "pointHoverBorderColor": 'rgba(54, 162, 235, 1)'
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": title or f"{value_col} Over {time_col}"
                    },
                    "legend": {
                        "display": True,
                        "position": "top"
                    }
                },
                "scales": {
                    "y": {
                        "beginAtZero": True,
                        "title": {
                            "display": True,
                            "text": str(value_col)
                        }
                    },
                    "x": {
                        "title": {
                            "display": True,
                            "text": str(time_col)
                        }
                    }
                }
            }
        }
        
        return chart_spec
        
    except Exception as e:
        return {"error": f"Failed to prepare line chart data: {str(e)}"}

def prepare_pie_chart_data(df, label_col, value_col, title=None, n=10):
    """
    Prepares pie chart data for frontend Chart.js rendering
    Returns structured JSON with chart specification
    """
    try:
        # Get top N values for pie chart
        top_data = df.sort_values(by=value_col, ascending=False).head(n)
        
        # Prepare labels and data
        labels = top_data[label_col].astype(str).tolist()
        values = top_data[value_col].tolist()
        
        chart_spec = {
            "type": "pie",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": str(value_col),
                    "data": values,
                    "backgroundColor": [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)',
                        'rgba(255, 159, 64, 0.8)',
                        'rgba(199, 199, 199, 0.8)',
                        'rgba(83, 102, 255, 0.8)',
                        'rgba(255, 99, 255, 0.8)',
                        'rgba(99, 255, 132, 0.8)'
                    ],
                    "borderColor": [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(199, 199, 199, 1)',
                        'rgba(83, 102, 255, 1)',
                        'rgba(255, 99, 255, 1)',
                        'rgba(99, 255, 132, 1)'
                    ],
                    "borderWidth": 1
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": title or f"Top {n} {label_col} by {value_col}"
                    },
                    "legend": {
                        "display": True,
                        "position": "right"
                    }
                }
            }
        }
        
        return chart_spec
        
    except Exception as e:
        return {"error": f"Failed to prepare pie chart data: {str(e)}"}
