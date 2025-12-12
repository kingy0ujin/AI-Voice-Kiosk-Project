import chromadb
from src.core.config import settings

class VectorDB:
    def __init__(self):
        # Use simple persist directory
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PATH)
        self.collection = self.client.get_or_create_collection(name="menu_items")
        self._initialize_db_if_empty()

    def _initialize_db_if_empty(self):
        if self.collection.count() == 0:
            print("Initializing Vector DB with Menu Items...")
            menus = [
                # Burgers
                {"id": "b1", "text": "불고기 버거: 한국적인 맛의 달콤한 불고기 소스가 듬뿍 들어간 베스트셀러 버거입니다. 가격 5000원.", "category": "버거", "name": "불고기 버거", "price": 5000},
                {"id": "b2", "text": "치즈 버거: 고소한 치즈가 패티 위에서 사르르 녹아내리는 클래식 버거입니다. 가격 5500원.", "category": "버거", "name": "치즈 버거", "price": 5500},
                {"id": "b3", "text": "새우 버거: 탱글탱글한 통새우 패티의 식감이 살아있는 프리미엄 버거입니다. 가격 6000원.", "category": "버거", "name": "새우 버거", "price": 6000},
                {"id": "b4", "text": "리얼 치즈 버거: 모짜렐라와 체다 치즈가 듬뿍 들어간 치즈 덕후를 위한 버거입니다. 가격 7000원.", "category": "버거", "name": "리얼 치즈 버거", "price": 7000},
                {"id": "b5", "text": "베이컨 버거: 바삭하게 구운 베이컨의 훈연 향이 입안 가득 퍼지는 버거입니다. 가격 6500원.", "category": "버거", "name": "베이컨 버거", "price": 6500},
                
                # Sides
                {"id": "s1", "text": "감자튀김: 갓 튀겨내어 바삭하고 짭조름한 프렌치 프라이입니다. 가격 2000원.", "category": "사이드", "name": "감자튀김", "price": 2000},
                {"id": "s2", "text": "양파링: 양파 본연의 단맛과 바삭한 튀김옷이 어우러진 사이드 메뉴입니다. 가격 2500원.", "category": "사이드", "name": "양파링", "price": 2500},
                {"id": "s3", "text": "치즈스틱: 쭉 늘어나는 스트링 치즈를 바삭하게 튀겨낸 인기 간식입니다. 가격 2000원.", "category": "사이드", "name": "치즈스틱", "price": 2000},

                # Drinks
                {"id": "d1", "text": "콜라: 톡 쏘는 탄산이 버거의 느끼함을 잡아주는 시원한 콜라입니다. 가격 1500원.", "category": "음료", "name": "콜라", "price": 1500},
                {"id": "d2", "text": "사이다: 깔끔하고 청량한 맛으로 누구에게나 사랑받는 사이다입니다. 가격 1500원.", "category": "음료", "name": "사이다", "price": 1500},
                {"id": "d3", "text": "오렌지 주스: 상큼한 오렌지 과즙이 가득한 건강한 주스입니다. 가격 2500원.", "category": "음료", "name": "오렌지 주스", "price": 2500},
                {"id": "d4", "text": "레모네이드: 레몬의 상큼함이 입안을 개운하게 해주는 시원한 음료입니다. 가격 3000원.", "category": "음료", "name": "레모네이드", "price": 3000},
            ]
            
            self.collection.add(
                documents=[m["text"] for m in menus],
                metadatas=[{"category": m["category"], "name": m["name"], "price": m["price"]} for m in menus],
                ids=[m["id"] for m in menus]
            )
            print(f"Added {len(menus)} items to Vector DB.")

    def query(self, query_text: str, n_results: int = 5):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        # Format results into a single context string
        context = ""
        if results['documents']:
            for doc in results['documents'][0]:
                context += f"- {doc}\n"
        return context
