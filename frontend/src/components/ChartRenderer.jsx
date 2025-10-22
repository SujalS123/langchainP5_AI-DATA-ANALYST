import React, { useRef, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Bar, Line, Pie } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const ChartRenderer = ({ chartSpecification, className = "" }) => {
  const chartRef = useRef(null);

  // Create a unique key based on the chart specification to force re-rendering
  const chartKey = React.useMemo(() => {
    if (!chartSpecification) return 'no-chart';
    if (typeof chartSpecification === 'string') {
      return `chart-${chartSpecification.substring(0, 50)}`;
    }
    return `chart-${JSON.stringify(chartSpecification).substring(0, 50)}`;
  }, [chartSpecification]);

  // If no chart specification, return null
  if (!chartSpecification) {
    return null;
  }

  // If there's an error in the chart specification
  if (chartSpecification.error) {
    return (
      <div className={`chart-error ${className}`}>
        <p style={{ color: 'red', textAlign: 'center' }}>
          Chart generation failed: {chartSpecification.error}
        </p>
      </div>
    );
  }

  // Handle string-based chart specifications
  let chartSpec = chartSpecification;
  if (typeof chartSpecification === 'string') {
    try {
      chartSpec = JSON.parse(chartSpecification);
    } catch (e) {
      return (
        <div className={`chart-error ${className}`}>
          <p style={{ color: 'red', textAlign: 'center' }}>
            Invalid chart specification format
          </p>
        </div>
      );
    }
  }

  // Validate chart specification
  if (!chartSpec.type || !chartSpec.data) {
    return (
      <div className={`chart-error ${className}`}>
        <p style={{ color: 'red', textAlign: 'center' }}>
          Invalid chart specification: missing type or data
        </p>
      </div>
    );
  }

  // Default chart options with responsive sizing
  const defaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: chartSpec.options?.plugins?.title?.text || 'Chart',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#ddd',
        borderWidth: 1,
      }
    },
    scales: chartSpec.type !== 'pie' ? {
      x: {
        grid: {
          display: false
        },
        title: {
          display: chartSpec.options?.scales?.x?.title?.display || false,
          text: chartSpec.options?.scales?.x?.title?.text || ''
        }
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)'
        },
        title: {
          display: chartSpec.options?.scales?.y?.title?.display || false,
          text: chartSpec.options?.scales?.y?.title?.text || ''
        }
      }
    } : undefined
  };

  // Merge with provided options
  const chartOptions = {
    ...defaultOptions,
    ...chartSpec.options,
    plugins: {
      ...defaultOptions.plugins,
      ...chartSpec.options?.plugins
    },
    scales: chartSpec.type !== 'pie' ? {
      ...defaultOptions.scales,
      ...chartSpec.options?.scales
    } : undefined
  };

  // Render the appropriate chart type
  const renderChart = () => {
    const chartHeight = 400; // Fixed height for consistency
    
    switch (chartSpec.type.toLowerCase()) {
      case 'bar':
        return (
          <div style={{ height: `${chartHeight}px` }} key={chartKey}>
            <Bar data={chartSpec.data} options={chartOptions} />
          </div>
        );
      case 'line':
        return (
          <div style={{ height: `${chartHeight}px` }} key={chartKey}>
            <Line data={chartSpec.data} options={chartOptions} />
          </div>
        );
      case 'pie':
        return (
          <div style={{ height: `${chartHeight}px` }} key={chartKey}>
            <Pie data={chartSpec.data} options={chartOptions} />
          </div>
        );
      default:
        return (
          <div className={`chart-error ${className}`} key={chartKey}>
            <p style={{ color: 'red', textAlign: 'center' }}>
              Unsupported chart type: {chartSpec.type}
            </p>
          </div>
        );
    }
  };

  return (
    <div className={`chart-container ${className}`} ref={chartRef} key={chartKey}>
      {renderChart()}
    </div>
  );
};

export default ChartRenderer;
