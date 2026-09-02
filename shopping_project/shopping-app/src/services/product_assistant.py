import re
from typing import List, Dict, Optional


class ProductAssistant:
    def __init__(self, products: List[Dict], reviews: Optional[List[Dict]] = None, orders: Optional[List[Dict]] = None):
        self.products = products or []
        self.reviews = reviews or []
        self.orders = orders or []

    @staticmethod
    def _normalize(value: str) -> str:
        return " ".join(re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).split())

    def _find_product(self, question: str) -> Optional[Dict]:
        q = self._normalize(question)
        best_match = None
        best_score = -1

        if not q:
            return None

        for product in self.products:
            name = self._normalize(str(product.get("name", "")))
            description = self._normalize(str(product.get("description", "")))
            haystack = f"{name} {description}"
            if not haystack:
                continue

            score = 0
            if q == name:
                score = 100
            elif name.startswith(q) or q.startswith(name):
                score = 80
            elif q in haystack:
                score = 70
            else:
                tokens = q.split()
                matches = sum(1 for token in tokens if token in haystack)
                if matches:
                    score = min(60, matches * 10)

            if score > best_score:
                best_match = product
                best_score = score

        if best_score >= 10:
            return best_match
        return None

    def _extract_price(self, question: str):
        match = re.search(r"(?:under|below|less than|up to|at most|<=)\s*(?:\$)?\s*(\d+(?:\.\d+)?)", question, re.IGNORECASE)
        if match:
            return float(match.group(1))

        match = re.search(r"(?:price|cost)\s*(?:is|of)?\s*(?:\$)?\s*(\d+(?:\.\d+)?)", question, re.IGNORECASE)
        if match:
            return float(match.group(1))

        return None

    def _short_product(self, product: Dict) -> str:
        name = product.get("name", "Unknown")
        price = product.get("price", 0)
        stock = product.get("stock", 0)
        return f"- {name}: ${price:.2f} | stock: {stock}"

    def _product_reviews(self, product_id: int) -> List[Dict]:
        return [r for r in self.reviews if int(r.get("product_id", -1)) == int(product_id)]

    def _review_summary_for_product(self, product: Dict) -> str:
        product_id = product.get("id")
        item_reviews = self._product_reviews(product_id)
        if not item_reviews:
            return f"{product.get('name')} has no reviews yet."

        avg = sum(int(r.get("rating", 0)) for r in item_reviews) / len(item_reviews)
        comments = [r.get("comment", "") for r in item_reviews if r.get("comment")]
        top_comment = comments[0] if comments else "No comments available."
        return (
            f"{product.get('name')} has {len(item_reviews)} review(s) with an average rating of {avg:.1f}/5. "
            f"Latest feedback: \"{top_comment}\""
        )

    def _product_orders(self, product_id: int) -> List[Dict]:
        return [o for o in self.orders if int(o.get("product_id", -1)) == int(product_id)]

    def answer(self, question: str) -> str:
        if not question or not question.strip():
            return "Please ask a question about the products in the store."

        q = question.strip()
        qn = self._normalize(q)

        if not self.products:
            return "There are no products in the catalog yet. Add a product first and then ask questions."

        if any(keyword in qn for keyword in ["show all products", "list products", "catalog", "what products", "available products"]):
            return "Available products:\n" + "\n".join(self._short_product(p) for p in self.products)

        if any(keyword in qn for keyword in ["cheapest", "lowest price", "least expensive"]):
            cheapest = min(self.products, key=lambda p: float(p.get("price", 0)))
            return f"The cheapest product is {cheapest.get('name')} at ${float(cheapest.get('price', 0)):.2f}."

        if any(keyword in qn for keyword in ["most expensive", "highest price", "expensive"]):
            priciest = max(self.products, key=lambda p: float(p.get("price", 0)))
            return f"The most expensive product is {priciest.get('name')} at ${float(priciest.get('price', 0)):.2f}."

        if "in stock" in qn or "available" in qn:
            available = [p for p in self.products if int(p.get("stock", 0)) > 0]
            if not available:
                return "There are currently no products in stock."
            return "In-stock products:\n" + "\n".join(self._short_product(p) for p in available)

        if any(keyword in qn for keyword in ["price", "cost"]) and "what" in qn:
            product = self._find_product(q)
            if product:
                return f"{product.get('name')} costs ${float(product.get('price', 0)):.2f}."
            return "I could not find that product. Try naming the product exactly."

        if any(keyword in qn for keyword in ["review", "reviews", "rating", "feedback", "customers say", "customer feedback", "customers feel", "customer feel", "think", "like", "liked", "feel about"]):
            product = self._find_product(q)
            if product:
                return self._review_summary_for_product(product)

            if "how many reviews" in qn or "number of reviews" in qn:
                for product in self.products:
                    if self._normalize(product.get("name", "")) in qn:
                        count = len(self._product_reviews(product.get("id")))
                        return f"{product.get('name')} has {count} review(s)."

            if "average rating" in qn or ("average" in qn and "rating" in qn):
                for product in self.products:
                    if self._normalize(product.get("name", "")) in qn:
                        item_reviews = self._product_reviews(product.get("id"))
                        if item_reviews:
                            avg = sum(int(r.get("rating", 0)) for r in item_reviews) / len(item_reviews)
                            return f"{product.get('name')} has an average rating of {avg:.1f}/5."
                        return f"{product.get('name')} has no reviews yet."

            if not product:
                return "I can summarize reviews for a specific product. Try asking about a product name such as 'Laptop' or 'Wireless Mouse'."

        if any(keyword in qn for keyword in ["order", "orders", "purchase", "purchased", "revenue", "sold", "status"]):
            if "how many orders" in qn or "number of orders" in qn or "total orders" in qn or "orders are there" in qn:
                return f"There are {len(self.orders)} order(s) in the store."

            if "total revenue" in qn or "revenue" in qn:
                total = sum(float(o.get("total_price", 0)) for o in self.orders)
                return f"Total revenue is ${total:.2f}."

            if "status" in qn or "order status" in qn:
                product = self._find_product(q)
                if product:
                    item_orders = self._product_orders(product.get("id"))
                    if item_orders:
                        latest = item_orders[-1]
                        return f"{product.get('name')} has order status: {latest.get('status', 'unknown')}."
                    return f"There are no orders for {product.get('name')} yet."
                return "I can check order status for a specific product. Try naming the product."

            product = self._find_product(q)
            if product:
                item_orders = self._product_orders(product.get("id"))
                if item_orders:
                    qty = sum(int(o.get("quantity", 0)) for o in item_orders)
                    return f"{product.get('name')} has {len(item_orders)} order(s) totaling {qty} unit(s)."
                return f"There are no orders for {product.get('name')} yet."

            return "I can answer order questions like total orders, revenue, and product order status. Try asking: 'How many orders are there?' or 'What is the status of the Laptop order?'"

        product = self._find_product(q)
        if product:
            name = product.get("name", "This product")
            price = float(product.get("price", 0))
            stock = int(product.get("stock", 0))
            description = product.get("description", "No description available.")
            return (
                f"{name} costs ${price:.2f}. It has {stock} unit(s) in stock. "
                f"Description: {description}"
            )

        budget = self._extract_price(qn)
        if budget is not None:
            matches = [p for p in self.products if float(p.get("price", 0)) <= budget]
            if matches:
                return "Products under that budget:\n" + "\n".join(self._short_product(p) for p in matches)
            return f"There are no products priced at or below ${budget:.2f}."

        return (
            "I can help with product prices, stock, descriptions, and the catalog. "
            "Try asking: 'What is the price of Laptop?', 'Show all products', or 'Which products are in stock?'"
        )
