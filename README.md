# Online_Shopping_Store

Welcome to the repository for the Online Shopping Store, a dynamic web application designed to emulate the functionalities of major e-commerce platforms like Amazon and Digikala. This project is built using Django and Django REST Framework, providing a robust backend structure that supports multiple users, including both buyers and sellers.

## Features

- **User Management**: Allows multiple users to register and manage their accounts.
- **Seller Dashboard**: Sellers can add and manage their products.
- **Product Listings**: Products are listed with features like descriptions, prices, and discounts.
- **Coupons and Discounts**: Users can apply discount codes at checkout for additional savings.

## Technologies

- **Django**: A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
- **Django REST Framework**: A powerful and flexible toolkit for building Web APIs.
- **Celery with Redis**: Used for background task processing and caching to enhance performance.
- **Other Dependencies**: See `requirements.txt` for a full list of dependencies.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- Python (3.8 or later)
- pip (Python package installer)
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/FardinMoghaddamPour/Online_Shopping_Store
```

then enter directory:

```bash
cd Online_Shopping_Store
```

Install the required package:

```bash
pip install -r requirements.txt
```

### Setting Up the Database

To set up your database and prepare the application for use, follow these steps:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create the necessary database tables according to the models defined in your Django application.

### Create User Groups

Run the following command to create predefined user groups, which help in assigning roles and permissions within the application:

```bash
python manage.py create_groups
```

### Running the Application

To start the Django development server and access the application on your local machine, execute:

```bash
python manage.py runserver
```

This command starts a web server that can be accessed at http://127.0.0.1:8000/, where you can view and interact with your application.

### Admin Setup

To configure roles for users, such as setting a user as a Product Manager, Supervisor, or Operator, use the following command format:

```bash
python manage.py set_rule -u {username} {flag}
```

for example:

```bash
python manage.py set_rule -u "John-Doe" -P
```

Flags for setting user roles:
- `-P` Assigns the Product Manager role
- `-S` Assigns the Supervisor role
- `-O` Assigns the Operator role

`Note: Due to current limitations of the command, only one role can be assigned at a time. If you need to assign multiple roles, you must run the command separately for each role.`

## Contributing

We welcome contributions from the community. Whether you're fixing bugs, adding new features, or improving documentation, your help is appreciated. To contribute:

1. Fork the project repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 (GPLv3). This license allows you to use, modify, and distribute the software, but any modifications or derivative works must also be shared under the same license. For more details, see the LICENSE file in the repository.

## Contact

If you have any questions, suggestions, or would like to contribute to the project, please feel free to reach out. You can contact me at [officialfardinzand@gmail.com](mailto:officialfardinzand@gmail.com), or message me directly on Telegram: [@IDoNotUseSemicolons](https://t.me/IDoNotUseSemicolons).

## Acknowledgements

- Thanks to the Django and Django REST Framework communities for their excellent documentation and resources.
- A special shoutout to all contributors and maintainers of the Celery and Redis projects, whose tools help improve the performance of our application.
- Special thanks to Mr. Yazdan ([@MrYazdan](https://github.com/MrYazdan)), Mr. Ghanavati ([@hosseinghanavati](https://github.com/hosseinghanavati)), and Mr. Ahmadi ([@MohamadAhmadi100](https://github.com/MohamadAhmadi100)) for their guidance and mentorship in my coding journey.

## Feedback

Your feedback is crucial in helping us improve this project. If you have any comments or suggestions, please open an issue in the GitHub repository, or better yet, submit a pull request with your proposed changes.

Thank you for your interest in the Online Shopping Store project!