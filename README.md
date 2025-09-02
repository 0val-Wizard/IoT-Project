# IoT-Project
- You can also read through my presentation slides for clearer summary.

- **Backgroud Context**: IoT Application Development (IoT) is a Year 2 module in TP. Which covers the concepts of Distributed System Architecture like Service-Oriented Architecture, Representational State Transfer (REST) and Web Services, identification of technology and design principles for connected devices as well as prototyping techniques for developing web services.

## AWS Services Used;
<img width="1432" height="856" alt="image" src="https://github.com/user-attachments/assets/94b96f88-d51d-4b74-a66e-a136a905a95b" />

## System Achitecture
<details>
  <summary>Sensor #1: HeartRate</summary>
  <img width="1360" height="912" alt="image" src="https://github.com/user-attachments/assets/986d4110-7d36-40e9-a0e1-95cbbd2c44a4" />
</details>

<details>
  <summary>Sensor #2: Temperature</summary>
  <img width="1114" height="894" alt="image" src="https://github.com/user-attachments/assets/3098c5a4-e52f-4c11-8a1a-2ff338e3ce0f" />
</details>

<details>
  <summary>Sensor #3: GPS</summary>
  <img width="1220" height="926" alt="image" src="https://github.com/user-attachments/assets/2b3fa58b-cccf-4f9a-a90c-b7cf92e024fa" />
</details>

<details>
  <summary>Sensor #4: Motion</summary>
  <img width="1146" height="884" alt="image" src="https://github.com/user-attachments/assets/cbf4c027-3780-419a-9d35-7ff784fd5a28" />
</details>

## AWS Service Screenshots
1. SNS
<img width="289" height="152" alt="image" src="https://github.com/user-attachments/assets/575fbdc5-1d50-4627-a9b9-72853a2e8f03" />
<img width="287" height="159" alt="image" src="https://github.com/user-attachments/assets/bbfe90fc-0f87-4b85-877b-d5232d2da4a2" />
<img width="288" height="150" alt="image" src="https://github.com/user-attachments/assets/f77bedb1-1e37-4d28-8915-60b4daf5450e" />


2. S3
Used for AWS SageMaker AI Service
<img width="430" height="200" alt="image" src="https://github.com/user-attachments/assets/9c31b47c-5144-4195-939c-4550a6ce94a3" />

3. API Gateway
Sends GPS data to the GPS_Map
<img width="430" height="214" alt="image" src="https://github.com/user-attachments/assets/bb32dd49-f201-48b0-881c-b1dd0d053a6f" />

4. AWS Location Service
GPS Map - Helps Locate Dog & alerts owner when pet in an 'Restricted Area'
<img width="506" height="274" alt="image" src="https://github.com/user-attachments/assets/6bf82aa1-3846-4c7e-bd1d-f798c8923787" />

5. AWS Timestream
<img width="421" height="170" alt="image" src="https://github.com/user-attachments/assets/7a69d912-6d23-4450-b67d-c87b25654a7a" />

6. AWS Kinesis
Stores data for Motion Data
<img width="430" height="114" alt="image" src="https://github.com/user-attachments/assets/63656459-493b-4ccd-8bfe-b7c36ec8c3de" />

