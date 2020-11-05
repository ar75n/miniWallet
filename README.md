

virtualenv venv -p python3.7
source venv/bin/activate
pip install -r requirements.txt

python manage.py makemigrations  
python manage.py migrate



*** For step 2 to step 6, use the token generated from step 1 in place of `Token <my token>`.

1. Initialize my account for wallet
curl --location --request POST 'http://localhost:8000/api/v1/init' \
--header 'Authorization: Token 6b3f7dc70abe8aed3e56658b86fa508b472bf238' \
--form 'customer_xid=wallet_1'

2. Enable my wallet 
curl --location --request POST 'http://localhost:8000/api/v1/wallet' \
--header 'Authorization:Token <my token>'

3. Disable my wallet
curl --location --request PATCH 'http://localhost:8000/api/v1/wallet' \
--header 'Authorization: Token <my token>' \
--form 'is_disabled=true'

4. View my wallet balance
curl --location --request GET 'http://localhost:8000/api/v1/wallet' \
--header 'Authorization:Token <my token>'

5. Add virtual money to my wallet
curl --location --request POST 'http://localhost:8000/api/v1/wallet/deposits' \
--header 'Authorization: Token <my token>' \
--form 'amount=100000' \
--form 'reference_id=50535246-dcb2-4929-8cc9-004ea06f5241' \
--form 'deposited_by=customer_1'

6. Use virtual money from my wallet
curl --location --request POST 'http://localhost:8000/api/v1/wallet/withdrawals' \
--header 'Authorization: Token <my token>' \
--form 'withdrawn_amount=50000' \
--form 'reference_id=50535246-dcb2-4929-8cc9-004ea06f5241' \
--form 'withdrawn_by=customer_1'
