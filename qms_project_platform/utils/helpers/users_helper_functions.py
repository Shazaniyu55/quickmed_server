import firebase_admin
from firebase_admin import auth, firestore
import logging





logger = logging.getLogger(__name__)

def authenticate_firebase_token(user_id, firebase_token):
    try:
        decoded_token = auth.verify_id_token(firebase_token)
        if decoded_token['uid'] == user_id:
            return True
        else:
            return False
    except auth.InvalidIdTokenError:
        return False
    except auth.ExpiredIdTokenError:
        return False
    except auth.RevokedIdTokenError:
        return False
    except auth.CertificateFetchError:
        return False

def verify_otp(phone_number, otp):
    try:
        verified_token = auth.verify_phone_number_verification_code(phone_number, otp)
        if verified_token:
            return True
        else:
            return False
    except auth.PhoneNumberVerificationError as e:
        print(f'OTP verification failed: {e}')
        return False




def reset_user_password(user_id, new_password):
    try:
        
        user = auth.get_user(user_id)
        updated_user = auth.update_user(
            user.uid,
            password=new_password,
        )
        return True, None, updated_user

    except auth.UserNotFoundError:
        return False, 'User not found'

    except auth.FirebaseError as e:
        return False, str(e)


def delete_file_from_firestore(collection_name, document_id):
    try:
       
        db = firestore.client()
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.delete()
        
        logger.info(f"Document '{document_id}' deleted successfully from collection '{collection_name}'")
        
    except Exception as e:
        logger.exception(f"Error deleting document '{document_id}' from collection '{collection_name}': {e}")
        raise e
    



def authenticate_phone_number(user_id, phone_number):
    try:
       
        verified_token = auth.verify_phone_number_verification_code(phone_number, user_id)
        if verified_token:
            return True
        else:
            return False
    except auth.PhoneNumberVerificationError as e:
        print(f'Phone number verification failed: {e}')
        return False




def calculate_wallet_balance(user_id):
    try:
        db = firestore.client()
        user_wallet_ref = db.collection('userswallet').document(user_id)
        user_wallet_data = user_wallet_ref.get().to_dict()

        
        if user_wallet_data:
            current_balance = user_wallet_data.get('balance', 0)
            top_up_amount = user_wallet_data.get('top_up_amount', 0)
            total_balance = current_balance + top_up_amount
            return {
                'current_balance': current_balance,
                'top_up_amount': top_up_amount,
                'total_balance': total_balance
            }
        else:
            return {"error": "User wallet data not found"}

    except Exception as e:
        return {"error": str(e)}
    



def get_user_wallet_from_firestore(user_id):
    try:
        
        db = firestore.client()
        user_ref = db.collection('userswallet').document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            wallet_data = user_doc.to_dict().get('wallet', {})
            return wallet_data
        else:
            logger.error(f"User document not found for user ID: {user_id}")
            return None 
    except Exception as e:
        logger.exception(f"An error occurred while fetching user wallet data for user ID: {user_id}, Error: {e}")
        return None






def calculate_withdrawal_amount(user_id, withdrawal_amount):
    try:
        user_wallet_data = get_user_wallet_from_firestore(user_id)

        
        if user_wallet_data:
            current_balance = user_wallet_data.get('current_balance', 500)
            if withdrawal_amount > 500 and withdrawal_amount <= current_balance:
                new_balance = current_balance - withdrawal_amount
                withdrawal_details = {
                    'user_id': user_id,
                    'current_balance': current_balance,
                    'withdrawal_amount': withdrawal_amount,
                    'new_balance': new_balance
                }
                return withdrawal_details
            else:
                return None 
        else:
            return None  
    except Exception as e:
        print(f"An error occurred while calculating withdrawal amount: {str(e)}")
        return None



