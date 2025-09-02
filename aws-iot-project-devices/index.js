// const awsIot = require('aws-iot-device-sdk');

// // Configuration for each device
// const devicesConfig = {
//   gps: {
//     keyPath: 'certs/gps/fee41548d6f5e376db2670b0ea1c372623cdabee1b2663609b01203a1a7be893-private.pem.key',
//     certPath: 'certs/gps/fee41548d6f5e376db2670b0ea1c372623cdabee1b2663609b01203a1a7be893-certificate.pem.crt',
//     caPath: 'certs/gps/AmazonRootCA1.pem',
//     clientId: 'GPS_Thing',
//     host: 'a2heouppm0pu48-ats.iot.us-east-1.amazonaws.com',
//   },
//   temperature: {
//     keyPath: 'certs/temperature/49cff0eb2d46ff0bb6a5ff03d57c0a1363823fed8390736f8f1785d3a481132e-private.pem.key',
//     certPath: 'certs/temperature/49cff0eb2d46ff0bb6a5ff03d57c0a1363823fed8390736f8f1785d3a481132e-certificate.pem.crt',
//     caPath: 'certs/temperature/AmazonRootCA1.pem',
//     clientId: 'Temp_Thing',
//     host: 'a2heouppm0pu48-ats.iot.us-east-1.amazonaws.com',
//   },
//   heartRate: {
//     keyPath: 'certs/heartrate/69928e2f60118dffebe6fad115711c530611a138b949d26e7ebfbe768aa48d28-private.pem.key',
//     certPath: 'certs/heartrate/69928e2f60118dffebe6fad115711c530611a138b949d26e7ebfbe768aa48d28-certificate.pem.crt',
//     caPath: 'certs/heartrate/AmazonRootCA1.pem',
//     clientId: 'Heartrate_Thing',
//     host: 'a2heouppm0pu48-ats.iot.us-east-1.amazonaws.com',
//   },
//   motion: {
//     keyPath: 'certs/motion/35029cf0d12d1d73f6608fe97ae87c3cb4207c6e9754cb14b3883cf270bac9e2-private.pem.key',
//     certPath: 'certs/motion/35029cf0d12d1d73f6608fe97ae87c3cb4207c6e9754cb14b3883cf270bac9e2-certificate.pem.crt',
//     caPath: 'certs/motion/AmazonRootCA1.pem',
//     clientId: 'Motion_Thing',
//     host: 'a2heouppm0pu48-ats.iot.us-east-1.amazonaws.com',
//   },
// };

// // House geofence boundaries
// const houseBounds = {
//   minLongitude: -73.985428,
//   maxLongitude: -73.984428,
//   minLatitude: 40.747817,
//   maxLatitude: 40.748817,
// };

// // Function to generate synthetic GPS data
// function generateGpsData() {
//   const isInside = Math.random() < 0.8; // 80% chance of staying inside

//   let longitude, latitude;
//   if (isInside) {
//     longitude = parseFloat((Math.random() * (houseBounds.maxLongitude - houseBounds.minLongitude) + houseBounds.minLongitude).toFixed(6));
//     latitude = parseFloat((Math.random() * (houseBounds.maxLatitude - houseBounds.minLatitude) + houseBounds.minLatitude).toFixed(6));
//   } else {
//     const offset = (Math.random() * 0.0015 + 0.0005) * (Math.random() < 0.5 ? -1 : 1);
//     longitude = parseFloat((houseBounds.minLongitude + offset).toFixed(6));
//     latitude = parseFloat((houseBounds.minLatitude + offset).toFixed(6));
//   }

//   return {
//     coordinates: [longitude, latitude], // [Longitude, Latitude] format
//     timestamp: Math.floor(Date.now() / 1000),
//   };
// }

// // Function to generate synthetic temperature data
// function generateTemperatureData() {
//   return {
//     temperature: parseFloat((Math.random() * 5 + 35).toFixed(2)), // Normal pet temperature range
//     timestamp: Math.floor(Date.now() / 1000),
//   };
// }

// // Function to generate synthetic heart rate data (with occasional abnormal values)
// function generateHeartRateData() {
//   let heart_rate;
//   if (Math.random() < 0.8) {
//     // 80% chance of normal heart rate
//     heart_rate = Math.floor(Math.random() * 60 + 60);
//   } else {
//     // 20% chance of abnormal heart rate (<60 or >120)
//     heart_rate = Math.random() < 0.5 ? Math.floor(Math.random() * 20 + 40) : Math.floor(Math.random() * 40 + 121);
//   }

//   return {
//     heart_rate,
//     timestamp: Math.floor(Date.now() / 1000),
//   };
// }

// // Function to generate synthetic motion data
// function generateMotionData() {
//   return {
//     acceleration_x: parseFloat((Math.random() * 4 - 2).toFixed(2)),
//     acceleration_y: parseFloat((Math.random() * 4 - 2).toFixed(2)),
//     acceleration_z: parseFloat((Math.random() * 4 - 2).toFixed(2)),
//     timestamp: Math.floor(Date.now() / 1000),
//   };
// }

// // Function to initialize a device with a specified interval
// function initializeDevice(config, deviceName, publishInterval) {
//   const device = awsIot.device(config);

//   device.on('connect', () => {
//     console.log(`[${deviceName}] Connected to AWS IoT Core`);

//     // Subscribe to topics
//     device.subscribe(`pawtracker/${deviceName.toLowerCase()}`);

//     // Publish synthetic data at the specified interval
//     setInterval(() => {
//       let data;
//       let topic = '';

//       switch (deviceName) {
//         case 'GPS_Thing':
//           data = generateGpsData();
//           topic = 'pawtracker/gps';
//           break;
//         case 'Temp_Thing':
//           data = generateTemperatureData();
//           topic = 'pawtracker/temperature';
//           break;
//         case 'Heartrate_Thing':
//           data = generateHeartRateData();
//           topic = 'pawtracker/heartrate';
//           break;
//         case 'Motion_Thing':
//           data = generateMotionData();
//           topic = 'pawtracker/motion';
//           break;
//       }

//       if (topic) {
//         device.publish(topic, JSON.stringify(data));
//         console.log(`[${deviceName}] Published to ${topic}:`, JSON.stringify(data));
//       }
//     }, publishInterval);
//   });

//   device.on('message', (topic, payload) => {
//     console.log(`[${deviceName}] Received message:`, topic, payload.toString());
//   });

//   device.on('error', (error) => {
//     console.error(`[${deviceName}] Error:`, error);
//   });
// }

// // Initialize devices with respective intervals
// initializeDevice(devicesConfig.gps, 'GPS_Thing', 30000); // 30 seconds
// initializeDevice(devicesConfig.temperature, 'Temp_Thing', 10000); // 10 seconds
// initializeDevice(devicesConfig.heartRate, 'Heartrate_Thing', 30000); // 30 seconds
// initializeDevice(devicesConfig.motion, 'Motion_Thing', 10000); // 10 seconds 






const awsIot = require('aws-iot-device-sdk');

// Configuration for each device
const devicesConfig = {
  gps: {
    keyPath: 'certs/gps/fee41548d6f5e376db2670b0ea1c372623cdabee1b2663609b01203a1a7be893-private.pem.key',
    certPath: 'certs/gps/fee41548d6f5e376db2670b0ea1c372623cdabee1b2663609b01203a1a7be893-certificate.pem.crt',
    caPath: 'certs/gps/AmazonRootCA1.pem',
    clientId: 'GPS_Thing',
    host: 'a2heouppm0pu48-ats.iot.us-east-1.amazonaws.com',
  },
  temperature: {
    keyPath: 'certs/temperature/49cff0eb2d46ff0bb6a5ff03d57c0a1363823fed8390736f8f1785d3a481132e-private.pem.key',
    certPath: 'certs/temperature/49cff0eb2d46ff0bb6a5ff03d57c0a1363823fed8390736f8f1785d3a481132e-certificate.pem.crt',
    caPath: 'certs/temperature/AmazonRootCA1.pem',
    clientId: 'Temp_Thing',
    host: 'a2heouppm0pu48-ats.iot.us-east-1.amazonaws.com',
  },
  heartRate: {
    keyPath: 'certs/heartrate/69928e2f60118dffebe6fad115711c530611a138b949d26e7ebfbe768aa48d28-private.pem.key',
    certPath: 'certs/heartrate/69928e2f60118dffebe6fad115711c530611a138b949d26e7ebfbe768aa48d28-certificate.pem.crt',
    caPath: 'certs/heartrate/AmazonRootCA1.pem',
    clientId: 'Heartrate_Thing',
    host: 'a2heouppm0pu48-ats.iot.us-east-1.amazonaws.com',
  },
  motion: {
    keyPath: 'certs/motion/35029cf0d12d1d73f6608fe97ae87c3cb4207c6e9754cb14b3883cf270bac9e2-private.pem.key',
    certPath: 'certs/motion/35029cf0d12d1d73f6608fe97ae87c3cb4207c6e9754cb14b3883cf270bac9e2-certificate.pem.crt',
    caPath: 'certs/motion/AmazonRootCA1.pem',
    clientId: 'Motion_Thing',
    host: 'a2heouppm0pu48-ats.iot.us-east-1.amazonaws.com',
  },
};

// House geofence boundaries
const houseBounds = {
  minLongitude: -73.985428,
  maxLongitude: -73.984428,
  minLatitude: 40.747817,
  maxLatitude: 40.748817,
};

// Function to generate synthetic GPS data
function generateGpsData() {
  const isInside = Math.random() < 0.8;
  let longitude, latitude;
  if (isInside) {
    longitude = parseFloat((Math.random() * (houseBounds.maxLongitude - houseBounds.minLongitude) + houseBounds.minLongitude).toFixed(6));
    latitude = parseFloat((Math.random() * (houseBounds.maxLatitude - houseBounds.minLatitude) + houseBounds.minLatitude).toFixed(6));
  } else {
    const offset = (Math.random() * 0.0015 + 0.0005) * (Math.random() < 0.5 ? -1 : 1);
    longitude = parseFloat((houseBounds.minLongitude + offset).toFixed(6));
    latitude = parseFloat((houseBounds.minLatitude + offset).toFixed(6));
  }
  return {
    device_id: 'GPS_Thing',  // Adding device identifier
    coordinates: [longitude, latitude],
    timestamp: Math.floor(Date.now() / 1000),
  };  
}

// Function to generate synthetic temperature data
function generateTemperatureData() {
  return {
    temperature: parseFloat((Math.random() * 5 + 35).toFixed(2)),
    timestamp: Math.floor(Date.now() / 1000),
    device_id: 'Temp_Thing'
  };
}


// Function to generate synthetic heart rate data
function generateHeartRateData() {
  let heart_rate;
  if (Math.random() < 0.8) {
    heart_rate = Math.floor(Math.random() * 60 + 60);
  } else {
    heart_rate = Math.random() < 0.5 ? Math.floor(Math.random() * 20 + 40) : Math.floor(Math.random() * 40 + 121);
  }
  return {
    heart_rate,
    timestamp: Math.floor(Date.now() / 1000),
  };
}

// Function to generate synthetic motion data
function generateMotionData() {
  return {
    acceleration_x: parseFloat((Math.random() * 4 - 2).toFixed(2)),
    acceleration_y: parseFloat((Math.random() * 4 - 2).toFixed(2)),
    acceleration_z: parseFloat((Math.random() * 4 - 2).toFixed(2)),
    timestamp: Math.floor(Date.now() / 1000),
  };
}

// Function to generate synthetic heart rate inference data
function generateHeartRateInferenceData() {
  return {
    weight: 10.0,
    age: 5,
    heart_rate: Math.floor(Math.random() * 60 + 60),
    ecg_mean: Math.floor(Math.random() * 50 + 50),
    ecg_max: Math.floor(Math.random() * 50 + 75),
    ecg_min: Math.floor(Math.random() * 50),
    total_bad_duration: Math.floor(Math.random() * 10),
    timestamp: Math.floor(Date.now() / 1000),
  };
}

// Function to initialize a device with a specified interval
function initializeDevice(config, deviceName, publishInterval) {
  const device = awsIot.device(config);
  device.on('connect', () => {
    console.log(`[${deviceName}] Connected to AWS IoT Core`);
    device.subscribe(`pawtracker/${deviceName.toLowerCase()}`);
    setInterval(() => {
      let data;
      let topic = '';
      switch (deviceName) {
        case 'GPS_Thing':
          data = generateGpsData();
          topic = 'pawtracker/gps';
          break;
        case 'Temp_Thing':
          data = generateTemperatureData();
          topic = 'pawtracker/temperature';
          break;
        case 'Heartrate_Thing':
          data = generateHeartRateInferenceData();
          topic = 'pawtracker/inference';
          break;
        case 'Motion_Thing':
          data = generateMotionData();
          topic = 'pawtracker/motion';
          break;
      }
      if (topic) {
        device.publish(topic, JSON.stringify(data));
        console.log(`[${deviceName}] Published to ${topic}:`, JSON.stringify(data));
      }
    }, publishInterval);
  });
  device.on('message', (topic, payload) => {
    console.log(`[${deviceName}] Received message:`, topic, payload.toString());
  });
  device.on('error', (error) => {
    console.error(`[${deviceName}] Error:`, error);
  });
}

// Initialize devices with respective intervals
initializeDevice(devicesConfig.gps, 'GPS_Thing', 30000); // 30 seconds
initializeDevice(devicesConfig.temperature, 'Temp_Thing', 10000); // 10 seconds
initializeDevice(devicesConfig.heartRate, 'Heartrate_Thing', 30000); // 30 seconds
initializeDevice(devicesConfig.motion, 'Motion_Thing', 10000); // 10 seconds

