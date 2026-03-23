import os
import json
import random
from werkzeug.utils import secure_filename

class AdManager:
    def __init__(self, data_file='ads.json', upload_folder='static/ads'):
        self.data_file = data_file
        self.upload_folder = upload_folder
        self.ads = self._load_ads()
        self._ensure_folders()

    def _ensure_folders(self):
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def _load_ads(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_ads(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.ads, f, indent=4)

    def add_ad(self, file_storage, target_age, target_gender):
        if not file_storage or file_storage.filename == '':
            return False, "No file provided"

        filename = secure_filename(file_storage.filename)
        # Create a unique filename to avoid overwrites
        import uuid
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(self.upload_folder, unique_filename)
        
        try:
            file_storage.save(filepath)
            ad_entry = {
                "id": str(uuid.uuid4()),
                "filename": unique_filename,
                "url": f"/{self.upload_folder}/{unique_filename}".replace('\\', '/'),
                "target_age": target_age, # 'Child', 'Teen', 'Adult', 'Senior', 'Any'
                "target_gender": target_gender # 'Male', 'Female', 'Any'
            }
            self.ads.append(ad_entry)
            self._save_ads()
            return True, "Ad added successfully"
        except Exception as e:
            return False, str(e)

    def get_all_ads(self):
        return self.ads

    def get_relevant_ad(self, age_category, gender):
        if not self.ads:
            return None # No ads in system
            
        exact_matches = []
        partial_matches = []
        generic_ads = []

        for ad in self.ads:
            is_age_exact = (ad['target_age'] == age_category)
            is_gender_exact = (ad['target_gender'] == gender)
            is_age_any = (ad['target_age'] == 'Any')
            is_gender_any = (ad['target_gender'] == 'Any')

            if is_age_exact and is_gender_exact:
                exact_matches.append(ad)
            elif (is_age_exact and is_gender_any) or (is_age_any and is_gender_exact):
                partial_matches.append(ad)
            elif is_age_any and is_gender_any:
                generic_ads.append(ad)
                
        # Prioritize exact matches over partial and generic ones
        if exact_matches:
            return random.choice(exact_matches)
        if partial_matches:
            return random.choice(partial_matches)
        if generic_ads:
            return random.choice(generic_ads)
            
        return random.choice(self.ads)

    def delete_ad(self, ad_id):
        ad_to_delete = None
        for ad in self.ads:
            if ad['id'] == ad_id:
                ad_to_delete = ad
                break
        
        if not ad_to_delete:
            return False, "Ad not found"
            
        try:
            # Optionally remove file
            filepath = os.path.join(self.upload_folder, ad_to_delete['filename'])
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Error removing file: {e}")
            
        self.ads = [ad for ad in self.ads if ad['id'] != ad_id]
        self._save_ads()
        return True, "Ad deleted"

    def edit_ad(self, ad_id, new_age, new_gender):
        for ad in self.ads:
            if ad['id'] == ad_id:
                ad['target_age'] = new_age
                ad['target_gender'] = new_gender
                self._save_ads()
                return True, "Ad updated"
        return False, "Ad not found"
