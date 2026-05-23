from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder

encoder=HuggingFaceEncoder(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)

faq=Route(
    name='faq',
    utterances=[
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
        "What if my product is defective?",
        "Can I replace damaged products?",
        "What if the item arrives broken?",
        "How do returns work?",
        "Can I return faulty products?",
        "What is your replacement policy?",
        "refund",
        "return",
        "damaged product",
        "broken item",
        "replacement",
        "faulty product",
        "refund policy",
        "return policy",
        "track my order",
        "payment methods",
        "cash on delivery",
        "COD available",
        "can I pay on delivery",
        "is cash on delivery available",
        "do you support COD",
        "can I use cash payment",
        "payment options",
        "online payment methods",

    ]
)
sql=Route(
    name='sql',
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",

    ]
)

smalltalk=Route(
    name='smalltalk',
    utterances=["Hi",
    "Hello",
    "Hey",
    "Good morning",
    "Good evening",
    "How are you?",
    "How’s it going?",
    "What’s up?",
    "What is your name?",
    "Who are you?",
    "What are you?",
    "What do you do?",
    "Can you help me?",
    "Are you a robot?",
    "Are you real?",
    "Nice to meet you",
    "Thank you",
    "Thanks",
    "Awesome",
    "Cool",
    "Bye",
    "Goodbye",
    "See you later",
    "Have a nice day",
    "You are smart",
    "You are helpful",
    "Tell me a joke",
    "What can you do?",
    "I need help",
    "Help me",]
)

router=SemanticRouter(routes=[faq,sql,smalltalk],encoder=encoder,auto_sync="local",top_k=1)

if __name__=="__main__":
    print(router("what is refund policy?").name)
    print(router("Pink Puma shoes in price range 5000 to 1000").name)