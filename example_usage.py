"""Example usage for Count-Min Sketch Skill."""
from client import CountMinSketch

def main():
    print("Executing Count-Min Sketch...")
    cms = CountMinSketch(width=500, depth=5)
    for _ in range(120):
        cms.update("HIGH_PRIORITY_TASK")
    for _ in range(25):
        cms.update("LOW_PRIORITY_TASK")

    est_high = cms.estimate("HIGH_PRIORITY_TASK")
    est_low = cms.estimate("LOW_PRIORITY_TASK")
    print(f"Estimates -> High: {est_high}, Low: {est_low}")
    assert est_high >= 120
    assert est_low >= 25
    print("Count-Min Sketch verified successfully!")

if __name__ == "__main__":
    main()
