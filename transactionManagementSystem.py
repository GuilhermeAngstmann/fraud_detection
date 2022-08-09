from datetime import datetime, timedelta
import numpy as np
import itertools

class customer:

    def __init__(self, first_name:str, last_name:str, email:str,  age:int, gender:str, street:str, education_level:str, credit_card_limit:float, account_status:bool) -> None:
        
        self.customer_account_id = email

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.age = age

        self.education_level = education_level
        self.street = street

        self.account_status = account_status
        self.credit_card_limit = credit_card_limit

        self.transactions_dict = {}

    def _calculate_status(self, transaction_datetime):

        additional_info = None

        if self.transactions_dict:
            status = 'NO_HISTORY'
            return status, additional_info
        
        n_frauds = sum(np.array(list(self.transactions_dict.values())) == 'FRAUD_REPORT')
        
        if n_frauds > 0:
            status = 'FRAUD_HISTORY'
            additional_info = n_frauds
            return status, additional_info

        days_ago = transaction_datetime - timedelta(89)
        n_purchases_prior = sum([
            1 for date, details in self.transactions_dict.items()
            if date < days_ago
            and details == 'PURCHASE'
        ])

        if n_purchases_prior > 0:
            status = 'GOOD_HISTORY'
            additional_info = n_purchases_prior
            return status, additional_info
        
        n_purchases = sum([
            1 for date, details in self.transactions_dict.items()
            if details == 'PURCHASE'
        ])

        if n_purchases > 0 and n_frauds == 0 and n_purchases_prior < 1:
            status = 'UNCONFIRMED_HISTORY'
            additional_info = n_purchases
            return status, additional_info

    def generate_summary(self, date):
        """Generates the summary given a date"""
        status, additional_info = self._calculate_status(date)
        formated_date = date.strftime('%Y-%m-%d')
        return formated_date, self.customer_account_id, {status: additional_info}

    def add_transaction(self, email:str, transaction_datetime:datetime, transaction_type:str, amount:float, category:str, merchant:str, purchase_location:str):
        if not email in set(self.customer_account_id.keys()):
            raise ValueError(f'Customer email not found in database: {email}')
        
        self.transactions_dict[transaction_datetime] = {
                                                        'type': transaction_type,
                                                        'amount':amount,
                                                        'category':category,
                                                        'merchant':merchant,
                                                        'purchase_location':purchase_location
                                                        }
    

class bankSystem(customer):
    def __init__(self) -> None:
        self.customers_dict = {}

    def add_customer(self, first_name:str, last_name:str, email:str,  age:int, gender:str, street:str, education_level:str, credit_card_limit:float, account_status: bool):
       
        if email not in set(self.customers_dict.keys()):
            self.customers_dict[email] = customer(
                                                first_name,
                                                last_name,
                                                email,
                                                age,
                                                gender,
                                                street,
                                                education_level,
                                                credit_card_limit,
                                                account_status)
        else:
            raise ValueError(f'the e-mail {email} is already in use.')

    def disable_customer(self, email):
        if email in set(self.customers_dict.keys()):
            self.customers_dict[email].account_status = False
        else:
            raise ValueError(f'the e-mail {email} doesn\'t exist on our base')
    
    def add_transaction(self, email:str, transaction_datetime:datetime, amount:float, category:str, merchant:str, purchase_location:str):
        """ transaction without user is not allowed

        Args:
            email (str): _description_
            transaction_datetime (datetime): _description_
            amount (float): _description_
            category (str): _description_
            merchant (str): _description_
            purchase_location (str): _description_
        """
        summary = self.customers_dict[email].add_transaction()


if __name__ == '__main__':
    import pandas as pd

    test_dict = {
        'first_name': ['joe'],
        'last_name': ['doe'],
        'email': ['joe.doe@email.com'],
        'age': [26],
        'gender': ['M'],
        'street': ['351 Darlene Green'],
        'education_level': ['BACHELORS OR EQUIVALENT LEVEL'],
        'credit_card_limit': [10000],
        'account_status': [True]
    }
    test_dataFrame = pd.DataFrame.from_dict(test_dict)


    bank = bankSystem()

    bank.add_customer(
        test_dataFrame['first_name'][0],
        test_dataFrame['last_name'][0],
        test_dataFrame['email'][0],
        test_dataFrame['age'][0],
        test_dataFrame['gender'][0],
        test_dataFrame['street'][0],
        test_dataFrame['education_level'][0],
        test_dataFrame['credit_card_limit'][0],      
        test_dataFrame['account_status'][0]
    )
