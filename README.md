# Problem Statement: Microservices Communication Using RabbitMQ

## Description
Build an inventory management system. The inventory management system aims to efficiently manage inventory items, track stock levels, and handle orders through a microservices architecture. The system will utilize RabbitMQ for inter-service communication and Docker for containerisation, ensuring scalability, modularity, and ease of deployment.

## Objectives
1. **Scalable Architecture:** Design a microservices architecture that allows independent development, deployment, and scaling of each component.
2. **Robust Communication:** Implement communication between microservices using RabbitMQ queues to ensure reliable message passing.
3. **Functional Microservices:** Develop microservices to handle specific tasks such as health checks, item creation, stock management, and order processing.
4. **Database Integration:** Integrate a database service to store inventory data and ensure proper CRUD operations.
5. **Containerization:** Containerize the application using Docker to provide consistency and portability across different environments.
6. **Testing and Documentation:** Conduct thorough testing to ensure the system functions as expected and provide comprehensive documentation for setup, usage, and maintenance.


# Technologies Used
The technologies used in this project include:

- RabbitMQ: A message broker that enables communication between microservices.
- Docker: A containerization platform used for packaging and deploying the application.
- Flask: A web framework for building HTTP servers and implementing RESTful APIs.
- MySQL: A database to store our data.


# Sample Flow Diagram
<p align="center">
  <img src="https://github.com/AshishBinoy/PES2UG21CS089_PES2UG21CS090_PES2UG21CS099_PES2UG21CS110_InventoryManagementSystem/assets/97509105/1afbd63f-72d0-457a-a1e1-d128beed6c65" />
</p>


# Deliverables

## Week 1: Setup and Basic Implementation

### Setup Docker Environment
- Create Dockerfiles for each microservice.
- Write a docker-compose.yml file to define the services and network configurations.
- Test Docker setup locally to ensure containers can communicate with each other.

### Implement RabbitMQ Communication
- Set up RabbitMQ container and network.
- Implement basic RabbitMQ communication between producer and consumer services.
- Test message passing between microservices via RabbitMQ queues.

### Develop HTTP Servers
- Choose a suitable web framework (e.g., Flask for Python) for implementing HTTP servers.
- Implement HTTP endpoints for health checks, and CRUD operations related to inventory management.
- Test HTTP servers locally to ensure they are functional.

## Week 2: Microservices Development

### Producer Service
- Develop the producer service responsible for constructing queues/exchanges and transferring data to consumers.
- Implement the HTTP server to listen to health_check and CRUD requests.
- Test the producer service to ensure it interacts correctly with RabbitMQ and handles HTTP requests.

### Consumer Services
- Implement consumer services (consumer_one to consumer_four) to handle specific tasks like health checks, item creation, stock management, and order processing.
- Ensure each consumer service can communicate with RabbitMQ and perform its designated actions.
- Test each consumer service individually to verify its functionality.

## Week 3: Integration and Testing

### Integration Testing
- Integrate all microservices into the Docker environment.
- Perform end-to-end testing to ensure seamless communication between microservices via RabbitMQ queues.
- Test various scenarios to ensure the proper functioning of the inventory management system.

## Sample file structure:
```
├── <microservices-project-directory>
    ├── docker-compose.yml
    ├── producer
    │   ├── producer.py
    │   ├── Dockerfile
    │   └──requirements.txt
    ├── consumer_one
    │   ├── healthcheck.py
    │   ├── Dockerfile
    │   └──requirements.txt
    ├── consumer_two
    │   ├── item_creation.py
    │   ├── Dockerfile
    │   └──requirements.txt
    ├── consumer_three
    │   ├── stock_management.py
    │   ├── Dockerfile
    │   └──requirements.txt
    ├── consumer_four
    │   ├── orderproccessing.py
    │   ├── Dockerfile
    │   └──requirements.txt
    └── database_service
```

# How to run the project

## Installation
- Clone the repository to your local machine.
```bash
git clone https://github.com/AshishBinoy/Microservices-Communication-Using-RabbitMQ.git
```
- Navigate to the project directory.
```bash
cd Microservices-Communication-Using-RabbitMQ
```
- Run the Docker Compose command to build and start the services.
> Ensure you have Docker installed on your machine.
```bash
docker-compose up --build
```
## Running the Services
- Once the services are up and running, you can access the HTTP endpoints of the producer service and interact with the inventory management system.
> The producer service will be available at [`http://localhost:5000`]
> RabbitMQ management console will be available at [`http://localhost:15672`]

### Health Check
- Check the health status of the producer service.
```bash
curl http://localhost:5000/health_check
```
> You should receive a response indicating the health status of the producer service.
> If the producer service is healthy, you can proceed to interact with other endpoints.

### CRUD Operations

#### Create an Item
- Create a new item in the inventory.
```bash
curl http://localhost:5000/insert/23/Apples/10/100
```
> This command will create an item with ID 23, name "Apples", price 10, and stock quantity 100.

#### Delete an Item
- Delete an item from the inventory.
```bash
curl http://localhost:5000/delete/23
```
> This command will delete the item with ID 23 from the inventory.

#### Update an Item
- Update the quantity of an item in the inventory.
```bash
curl http://localhost:5000/update/23/50
```
> This command will update the quantity of the item with ID 23 to 50.

#### Process an Order
- Process an order for an item.
```bash
curl http://localhost:5000/process/1/23/5
```
> This command will process an order with ID 1 for 5 units of the item with ID 23.