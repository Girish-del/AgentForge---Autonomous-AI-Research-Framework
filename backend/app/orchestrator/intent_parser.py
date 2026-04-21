class IntentParser:
    def parse(self, statement: str) -> dict[str, str]:
        text = statement.lower()
        task_type = "image_classification"
        if "detect" in text:
            task_type = "object_detection"
        return {"task_type": task_type}
