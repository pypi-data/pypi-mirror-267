import requests
from pydantic import BaseModel, ValidationError, validator
from typing import Optional


class SMSModel(BaseModel):
    destination_number: str
    message: str
    source_number: Optional[str] = None

    @validator('destination_number')
    def validate_destination_number(cls, v):
        if not v.isdigit():
            raise ValueError('Destination number must contain only digits')
        if len(v) < 10 or len(v) > 15:
            raise ValueError('Destination number length must be between 10 and 15 digits')
        return v

    @validator('message')
    def validate_message_length(cls, v):
        if len(v) > 160:
            raise ValueError('Message must not exceed 160 characters')
        return v

class Chromastone:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.base_url = 'https://chromastone-production.up.railway.app'
        
    
    def check_balance(self) -> str:
        '''this function will be used to check the balance of the user, it will return the balance as a string,'''


        full_url = self.base_url + '/check_balance'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        try:
            res = requests.post(url=full_url, headers=headers, json={'api_key': self.api_key})
            if res.status_code != 200:
                print('Failed to check balance, check your api key or internet. Status code:', res.status_code)
                return 'Failed to check balance, check your api key or internet connection'
            self.balance = res.json()['balance']
            return str(self.balance)
        except Exception as e:
            return e

    def buy_sms(self, amount: int) -> None:
        '''this function will be used to buy more sms but it is not implemented yet,'''

        return 'This function is not implemented yet'
        

    def send_sms(self, source_number: str, destination_number: str, message: str):
        '''destination_number must be of the form 263xxxxxxxxx, message must not exceed 120 characters, source_number is optional, it is the number that will be displayed as the sender of the SMS, it must be of the form 263xxxxxxxxx, if it is not provided, the default sender number will be used.'''
        full_url = self.base_url + '/send_sms'
        headers = {'Authorization': f'Bearer {self.api_key}',
                   'Content-Type': 'application/json'}
        # check if the user has enough balance to send the SMS
        balance = self.check_balance()
        if balance == 'Failed to check balance, check your api key or internet connection':
            raise Exception('Failed to check balance, check your api key or internet connection')
        else:
            balance = int(balance)
        if balance > 0:
            try:
                sms = SMSModel(source_number=source_number, destination_number=destination_number, message=message)
                sms_data = sms.dict()
                response = requests.post(url=full_url, data=sms_data, headers=headers)
                if response.status_code == 200:
                    print('SMS sent successfully, remaining balance:', response.json()['balance'])
                    return 'SMS sent successfully'
                else:
                    print('Failed to send SMS, status code:', response.status_code)
                    return 'Failed to send SMS'
            except ValidationError as e:
                print(e.json())
                return f"Failed to send SMS, {e.json()}"
        else:
            return 'You do not have enough balance to send the SMS'
        
    def send_innbucks(self, destination_number: str, message: str):
        '''send InnBucks to a user, destination_number must be of the form 263xxxxxxxxx, message must not exceed 120 characters.'''
        full_url = self.base_url + '/send_innbucks'
        headers = {'Authorization': f'Bearer {self.api_key}',
                   'Content-Type': 'application/json'}
        # check if the user has enough balance to send the SMS
        balance = self.check_balance()
        if balance == 'Failed to check balance, check your api key or internet connection':
            raise Exception('Failed to check balance, check your api key or internet connection')
        else:
            balance = int(balance)
        if balance > 0:
            try:
                sms = SMSModel(destination_number=destination_number, message=message)
                sms_data = sms.dict()
                response = requests.post(url=full_url, data=sms_data, headers=headers)
                if response.status_code == 200:
                    print('Innbucks sent successfully, remaining balance:', response.json()['balance'])
                    return 'Innbucks sent successfully'
                else:
                    print('Failed to send Innbucks, status code:', response.status_code)
                    return 'Failed to send Innbucks'
            except ValidationError as e:
                print(e.json())
                return f"Failed to send Innbucks, {e.json()}"
            
    def send_mukuru(self, destination_number: str, message: str):
        '''send mukuru to a user, destination_number must be of the form 263xxxxxxxxx, message must not exceed 120 characters.'''
        full_url = self.base_url + '/send_mukuru'
        headers = {'Authorization': f'Bearer {self.api_key}',
                   'Content-Type': 'application/json'}
        # check if the user has enough balance to send the SMS
        balance = self.check_balance()
        if balance == 'Failed to check balance, check your api key or internet connection':
            raise Exception('Failed to check balance, check your api key or internet connection')
        else:
            balance = int(balance)
        if balance > 0:
            try:
                sms = SMSModel(destination_number=destination_number, message=message)
                sms_data = sms.dict()
                response = requests.post(url=full_url, data=sms_data, headers=headers)
                if response.status_code == 200:
                    print('mukuru sent successfully, remaining balance:', response.json()['balance'])
                    return 'mukuru sent successfully'
                else:
                    print('Failed to send mukuru, status code:', response.status_code)
                    return 'Failed to send mukuru'
            except ValidationError as e:
                print(e.json())
                return f"Failed to send mukuru, {e.json()}"
    


