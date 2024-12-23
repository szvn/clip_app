import React, { useState, useRef, useEffect } from 'react';
import axiosInstance from './axiosConfig';
import Chart from 'chart.js/auto';
import { Button, TextField, Container, Typography, Box, Stack } from '@mui/material';
import { GoogleAuth } from 'google-auth-library'; // Import GoogleAuth library

function App() {
  const [image, setImage] = useState(null);
  const [textFields, setTextFields] = useState(['']);
  const [chartData, setChartData] = useState(null);

  // Function to fetch the identity token
  const getIdToken = async () => {
    try {
      const auth = new GoogleAuth();
      const client = await auth.getClient(); // Get the client for auth
      const targetAudience = process.env.REACT_APP_API_URL || 'http://localhost:8080/run/'; // Backend URL
      const idToken = await client.fetchIdToken(targetAudience); // Fetch the identity token
      return idToken;
    } catch (error) {
      console.error('Error fetching identity token:', error);
      return null;
    }
  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result.split(',')[1]); // Store the image base64 data
      };
      reader.readAsDataURL(file);
    }
  };

  const handleAddTextField = () => {
    setTextFields([...textFields, '']);
  };

  const handleTextChange = (index, value) => {
    const newTextFields = [...textFields];
    newTextFields[index] = value;
    setTextFields(newTextFields);
  };

  const handleSubmit = async () => {
    const payload = {
      image,
      labels: textFields,
    };

    try {
      // Fetch the identity token before making the request
      const idToken = await getIdToken();
      if (!idToken) {
        console.error('Unable to fetch identity token');
        return;
      }

      const response = await axiosInstance.post('/', payload, {
        headers: {
          Authorization: `Bearer ${idToken}`, // Add the identity token to the Authorization header
        },
      });
      setChartData(response.data);
    } catch (error) {
      console.error('Error submitting data:', error);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 5 }}>
      <Typography variant="h4" gutterBottom>
        AI Image Classifier
      </Typography>

      <Stack spacing={2}>
        <Button
          variant="contained"
          component="label"
          color="primary"
          sx={{ display: 'none' }}  // Hide the default image upload button
        >
          Upload Image
          <input
            type="file"
            accept="image/*"
            hidden
            onChange={handleImageUpload}
          />
        </Button>

        <Button
          variant="contained"
          component="label"
          color="primary"
          sx={{
            fontSize: '14px',
            padding: '10px 15px',
          }}
        >
          Upload Image
          <input
            type="file"
            accept="image/*"
            hidden
            onChange={handleImageUpload}
          />
        </Button>

        {textFields.map((text, index) => (
          <TextField
            key={index}
            label={`Option ${index + 1}`}  // Updated label
            variant="outlined"
            value={text}
            onChange={(e) => handleTextChange(index, e.target.value)}
            size="small"  // Smaller text field
            fullWidth
          />
        ))}

        <Button
          variant="outlined"
          color="secondary"
          onClick={handleAddTextField}
          sx={{ fontSize: '12px', padding: '8px 12px' }}  // Adjusted button size
        >
          Add Text Field
        </Button>

        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          sx={{
            fontSize: '14px',
            padding: '10px 15px',
          }}
        >
          Submit
        </Button>
      </Stack>

      {chartData && (
        <Box sx={{ mt: 5 }}>
          <BarChart data={chartData} />
        </Box>
      )}
    </Container>
  );
}

const BarChart = ({ data }) => {
  const canvasRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    const ctx = canvasRef.current.getContext('2d');
    const labels = Object.keys(data);
    const values = Object.values(data);

    chartInstance.current = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Response Data',
            data: values,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            max: 1,
          },
        },
        plugins: {
          legend: {
            labels: {
              font: {
                size: 12,  // Adjusting chart legend font size to match design
              },
            },
          },
        },
        responsive: true,
      },
    });

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [data]);

  return <canvas ref={canvasRef}></canvas>;
};

export default App;
