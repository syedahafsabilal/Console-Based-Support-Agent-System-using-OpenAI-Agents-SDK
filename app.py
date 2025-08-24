#"Console-Based Support Agent System using OpenAI Agents SDK"

from typing import Optional
from pydantic import BaseModel

class UserContext(BaseModel):
    name: str
    is_premium_user: bool = False
    issue_type: Optional[str] = None

class Tools:
    @staticmethod
    def refund(context: UserContext):
        return f"Refund processed for {context.name}."

    @staticmethod
    def restart_service(context: UserContext):
        return "Service has been restarted successfully"

    @staticmethod
    def provide_info(context: UserContext):
        return "Here is some general information for you"

 
def is_refund_enabled(context:UserContext):
    return context.is_premium_user
       
def is_restart_enabled(context:UserContext):
    return context.issue_type == "technical"
     


class TriageAgent:
    def handoff(self, context:UserContext):
        if context.issue_type == "billing" :
            return BillingAgent()
        elif context.issue_type == "technical":
            return TechnicalAgent()
        else:
            return GeneralAgent()

class BillingAgent:
    def handle(self, context: UserContext):
        if is_refund_enabled(context):
            return Tools.restart_service(context)
        else:
            return 'Refund tool not available for this issue type'
    
class TechnicalAgent:
      def handle(self, context: UserContext):
        if is_restart_enabled(context):
            return Tools.restart_service(context)
        else:
            return 'Restart tool not available for this issue type'

class GeneralAgent:
      def handle(self, context: UserContext):
            return Tools.provide_info(context)

def main():
    print(" Welcome to Support Agent System ")
    name = input("Enter your name: ")
    premium_input = input("Are you a premium user?(yes/no): ").lower()
    is_premium = premium_input == "yes"

    print("Issue types: billing, technical, general")
    issue_type = input("Enter your issue type:").lower()

    context = UserContext(name=name, is_premium_user=is_premium, issue_type=issue_type)

    triage = TriageAgent()
    agent  = triage.handoff(context)

    print(f"\n[Handoff] Triage Agent routed you to: {agent.__class__.__name__}")

    result = agent.handle(context)
    print(f"[Agent Response] {result}")

if __name__ =="__main__":
    main()