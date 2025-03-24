from datetime import datetime
from typing import Dict, List

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
        

    def add_request(self, ticket_id, sender,email_subject, email_body, classification_info):
        """Store a new service request in memory"""
        if ticket_id in self.requests:
            raise ValueError(f"Ticket ID {ticket_id} already exists")
            
        self.requests[ticket_id] = {
            "ticket_id": ticket_id,
            "email_subject": email_subject,
            "email_body": email_body,
            "sender": sender,
            "classification_info": classification_info,
            "timestamp": datetime.now().isoformat(),
            "status": "new",
            "thread": [],
            "classification_history":[]
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

    def _add_thread_message(self, ticket_id: str, email_subject: str,
                           email_body: str) -> bool:
        """Internal method to handle thread updates"""
        if ticket_id not in self.requests:
            return False
            
        ticket = self.requests[ticket_id]
        ticket["thread"].append({
            "subject": email_subject,
            "body": email_body,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update classification with latest analysis
        ticket["classification_history"].append(ticket["classification_info"])
        ticket["status"] = "updated"
        self._update_metadata()
        return True
    
    def update_request_with_thread(self, ticket_id, classification_info, email_subject: str, 
                 email_body: str):
        """Update request status"""
        if ticket_id in self.requests:
            _add_thread_message(ticket_id,email_subject, email_body)
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

    def _update_metadata(self):
        """Update storage statistics"""
        self.metadata["total_requests"] = len(self.requests)
        self.metadata["last_updated"] = datetime.now().isoformat()

    def get_all_ticket_data(self) -> List[dict]:
        """Return all tickets in standardized format"""
        result = []
        for ticket_id, ticket in self.requests.items():
        
            ticket_data = {
                "id": ticket_id,
                "email_subject": ticket["email_subject"],
                "email_body":ticket["email_body"],
                "sender":ticket["sender"],
                "is_duplicate": False,
                "classifications": ticket['classification_info']['classifications'],
                "thread": ticket['thread'],
                "summary": ticket['classification_info']["summary"],
                "additional_fields": ticket['classification_info']["additional_fields"],
                "classification_history": ticket['classification_history'],
                "status": ticket['status']
            }
            result.append(ticket_data)
        return result

    # Add this new method for complete data export
    def export_all_data(self) -> List[dict]:
        """Get complete ticket data including thread history"""
        return [
            {
                "id": ticket_id,
                "email_subject": ticket["email_subject"],
                "email_body":ticket["email_body"],
                "sender":ticket["sender"],
                "is_duplicate": false,
                "classifications": ticket['classification_info']['classifications'],
                "thread": ticket['thread'],
                "additional_fields": ticket['classification_info']["additional_fields"],
                "classification_history": ticket['classification_history'],
                "status": ticket['status']
            }
            for ticket_id, ticket in self.requests.items()
        ]
        