from datetime import datetime

class VolumeTracker:
    def __init__(self, data_type):
        self.data_type = data_type
        self.total_volume = 0.0
        self.valid_days_count = 0
        self.current_month = None
        self.processed_timestamps = set()

    def process_data(self, date_str, daily_volume, ydaily_volume):
        date = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S')

        if date_str in self.processed_timestamps:
            return
        
        self.processed_timestamps.add(date_str)
        
        if self.current_month != date.month:
            self.total_volume = 0.0
            self.valid_days_count = 0
            self.current_month = date.month

        if date.day == 1:
            if daily_volume != 0:
                self.total_volume += daily_volume
                self.valid_days_count += 1
        else:
            if ydaily_volume != 0:
                self.total_volume += ydaily_volume
                self.valid_days_count += 1

    def get_monthly_average(self):
        if self.valid_days_count == 0:
            return 0
        return self.total_volume / self.valid_days_count
