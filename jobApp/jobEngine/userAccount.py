class User:
    def __init__(self, username):
        self.username = username
        self.applications_used = 0
        self.days_left = 7
    
    def can_apply(self):
        return self.days_left > 0 and self.applications_used < self.max_applications_per_day()
    
    def apply(self):
        if self.can_apply():
            self.applications_used += 1
            if self.applications_used == self.max_applications_per_day():
                self.applications_used = 0
                self.days_left -= 1
            return True
        else:
            return False
        
    def max_applications_per_day(self):
        return 10 if self.days_left > 0 else 0


class FreeUser(User):
    def __init__(self, username):
        super().__init__(username)
        self.premium = False
        
    def can_apply(self):
        return not self.premium and super().can_apply()
    
    def upgrade(self, plan):
        if not self.premium:
            if plan == "50":
                self.premium = True
                self.max_applications_per_day = lambda: 50
            elif plan == "100":
                self.premium = True
                self.max_applications_per_day = lambda: 100
            elif plan == "unlimited":
                self.premium = True
                self.max_applications_per_day = lambda: float("inf")
            else:
                raise ValueError("Invalid plan")
        

class PremiumUser(User):
    def __init__(self, username, max_applications_per_day):
        super().__init__(username)
        self.max_applications_per_day = lambda: max_applications_per_day
