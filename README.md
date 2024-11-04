# Store management system

The primary goals of the project are:

- to implement web services that form the given system,
- to launch the system using container orchestration tools.

The system is designed for multi-user operations. Part of the system's functionality is publicly accessible, while other functions are available only to users who can log into the system. The system is implemented using the Python programming language, the Flask framework, and the SQLAlchemy library. SQLAlchemy is heavily used in processing user requests. Docker Image templates have been created to represent parts of the system and are used to launch the appropriate containers. A configuration file has also been written to launch the entire system using orchestration tools.
## Conceptual Description of the System
The system provides user registration (either as a customer or courier). Customers can search for products and place orders, while couriers can deliver these orders.

When the system is launched, accounts for all store owners are pre-provisioned. Store owners have the ability to add products and review sales statistics.

Each user must be registered before using the system. The following information is stored within each user’s account: email address and password used for login, first and last name, and user role. A user can have the role of a customer, store owner, or courier.

For products, the system stores information such as the category the product belongs to, product name, and its price. The product name must be unique. For each category, only its name is stored.

Customers can search for products, place orders, and view their order history.

For every product purchase, an order is created in the system. Each order includes a list of products, the total order price, its status, and the time of its creation. Initially, an order is in the "pending" status until picked up by a courier, at which point it changes to "in transit." Once the courier delivers the order to the customer, its status is updated to "completed."