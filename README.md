# CollabX

CollabX is an influencer marketing platform built with Django, designed to connect brands with creators for streamlined and effective collaborations. This platform simplifies the process of managing campaigns, fostering collaborations, and ensuring secure payments through Razorpay integration.

## Features

### For Brands
1. **Brand Registration and Login**: Easy account creation and secure login process.
2. **Profile Management**: Create and update brand profiles.
3. **Influencer Discovery**: Search and filter through a list of influencers/creators.
4. **Collaboration Requests**: View influencer profiles, show interest, and propose collaborations.
5. **Campaign Management**:
   - Add campaign details.
   - View and review influencer proposals.
   - Accept the best proposal and reject others.
   - View all influencers working on a specific campaign via the campaign details page.
6. **Secure Payments with Razorpay**: 
   - Use an escrow system to ensure influencers are paid only after successful campaign completion.

### For Creators
1. **Creator Registration and Login**: Easy account creation and secure login process.
2. **Profile Management**: Build and maintain a detailed influencer profile, including past campaign details.
3. **Campaign Discovery**: Browse and filter campaigns that match your niche.
4. **Proposal Submission**: View campaign details and show interest by submitting proposals.
5. **Campaign Tracking**:
   - View all campaigns you’ve shown interest in.
   - Track campaign status (Pending, Accepted, Rejected, Working, Completed).
   - Receive notifications on accepted campaigns.
6. **Campaign Reporting**: Submit campaign reports upon completion.
7. **Secure Payments with Razorpay**: Get paid securely after successfully completing a campaign.

## Installation and Setup

### Prerequisites
- Python 3.8+
- Django 4.x
- Razorpay API keys (create an account at [Razorpay](https://razorpay.com))
- Virtual Environment

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/rebin03/CollabX.git
   ```

2. Navigate to the project directory:
   ```bash
   cd CollabX
   ```

3. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate # For Linux/macOS
    venv\Scripts\activate # For Windows
   ```

4. Install dependencies:
    ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the root directory and add the following details:
   ### Django key
    - `SECRET_KEY`
    - `DEBUG`

    ### Email configuration
    - `EMAIL_HOST_PASSWORD`

    ### Razorpay keys
    - `RZP_KEY_ID`
    - `RZP_KEY_SECRET`

6. Run migrations:
    ```bash
   python manage.py migrate
   ```

7. Start the server:
    ```bash
   python manage.py runserver
   ```

8. Open the app in your browser at http://127.0.0.1:8000.


## Razorpay Integration
The platform uses Razorpay for secure payment processing. Payments are held in escrow and are only released to the influencer upon successful campaign completion.

## Usage

### For Brands
- Register and create a brand profile.
- Discover creators and propose collaborations.
- Manage campaigns and track collaborations.
- Use Razorpay for secure payments.

### For Creators
- Register and build your influencer profile.
- Explore available campaigns and submit proposals.
- Manage ongoing and completed campaigns.
- Receive payments securely through Razorpay.

## Technologies Used
- **Backend**: Python, Django
- **Frontend**: Django Templates
- **Database**: SQLite (default, can be replaced with PostgreSQL/MySQL)
- **Payment Gateway**: Razorpay
- **Environment Variables**: Managed using `.env` for sensitive data.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
