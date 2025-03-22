from datetime import datetime

class SRMemoryStorage:
    _instance = None  # Singleton pattern
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.requests = {}
        self.metadata = {
            "total_requests": 0,
            "last_updated": None,
            "created_at": datetime.now().isoformat()
        }

    def add_request(self, ticket_id, email_subject, email_body, classification_info):
        """Store a new service request in memory"""
        if ticket_id in self.requests:
            raise ValueError(f"Ticket ID {ticket_id} already exists")
            
        self.requests[ticket_id] = {
            "ticket_id": ticket_id,
            "email_subject": email_subject,
            "email_body": email_body,
            "classification_info": classification_info,
            "timestamp": datetime.now().isoformat(),
            "status": "new"
        }
        
        self.metadata["total_requests"] += 1
        self.metadata["last_updated"] = datetime.now().isoformat()
        return True

    def get_request(self, ticket_id):
        """Get request by ticket ID"""
        return self.requests.get(ticket_id)

    def get_all_requests(self, status_filter=None):
        """Get requests with optional status filter"""
        if status_filter:
            return {k: v for k, v in self.requests.items() 
                    if v["status"] == status_filter}
        return self.requests.copy()

    def update_request(self, ticket_id, classification_info):
        """Update request status"""
        if ticket_id in self.requests:
            self.requests[ticket_id]["status"] = "updated"
            self.requests[ticket_id]["classification_info"] = classification_info 
            self.metadata["last_updated"] = datetime.now().isoformat()
            return True
        return False

    @property
    def total_requests(self):
        return self.metadata["total_requests"]

    @property
    def last_updated(self):
        return self.metadata["last_updated"]

    def clear_storage(self):
        """Reset storage (for testing)"""
        self._initialize()