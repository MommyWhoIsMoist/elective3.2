import pandas as pd
import matplotlib.pyplot as plt

def quicksort(data, ascending=True):
    if len(data) <= 1:
        return data
    pivot = data[0]
    rest = data[1:]
    if ascending:
        left = [x for x in rest if x[1] < pivot[1]]
        right = [x for x in rest if x[1] >= pivot[1]]
    else:
        left = [x for x in rest if x[1] > pivot[1]]
        right = [x for x in rest if x[1] <= pivot[1]]
    return quicksort(left, ascending) + [pivot] + quicksort(right, ascending)

def load_data():
    df = pd.read_csv("data/export-2025-04-15T19_02_18.067Z.csv", skiprows=2)
    df.columns = ["Country", "Gender_Wage_Gap"]
    df.dropna(inplace=True)
    df["Gender_Wage_Gap"] = pd.to_numeric(df["Gender_Wage_Gap"], errors='coerce')
    df.dropna(inplace=True)
    return df

def display_menu():
    print("\n📊 Gender Wage Gap Analysis Menu:")
    print("1 - Sort countries by wage gap (High ↔ Low)")
    print("2 - Top 10 countries with largest wage gaps")
    print("3 - Top 10 countries with smallest wage gaps")
    print("4 - Compare to OECD average")
    print("5 - Show horizontal bar chart of wage gaps")
    print("0 - Exit")

def option_sort(df, ascending):
    data = list(zip(df["Country"], df["Gender_Wage_Gap"]))
    sorted_data = quicksort(data, ascending)
    print(f"\n{'Ascending' if ascending else 'Descending'} sorted countries by gender wage gap:")
    for country, gap in sorted_data:
        print(f"{country}: {gap:.2f}%")
    return not ascending  # toggle

def option_top_largest(df):
    top = df.sort_values(by="Gender_Wage_Gap", ascending=False).head(10)
    print("\nTop 10 countries with the largest gender wage gaps:")
    print(top.to_string(index=False))

def option_top_smallest(df):
    bottom = df.sort_values(by="Gender_Wage_Gap", ascending=True).head(10)
    print("\nTop 10 countries with the smallest gender wage gaps:")
    print(bottom.to_string(index=False))

def option_compare_oecd(df):
    oecd = df[df["Country"].str.strip().str.upper() == "OECD"]
    if not oecd.empty:
        avg = oecd["Gender_Wage_Gap"].values[0]
        print(f"\nOECD average gender wage gap: {avg:.2f}%")
    else:
        print("\nOECD data not found in the dataset.")

def option_plot(df):
    plt.figure(figsize=(10, 8))
    sorted_df = df.sort_values(by="Gender_Wage_Gap", ascending=False)
    plt.barh(sorted_df["Country"], sorted_df["Gender_Wage_Gap"], color="skyblue")
    plt.xlabel("Gender Wage Gap (%)")
    plt.title("Gender Wage Gap by Country")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def main():
    print("\n=== Running Dataset 2 Analysis ===")
    try:
        df = load_data()
        ascending = False  # default sort order

        while True:
            display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                ascending = option_sort(df, ascending)
            elif choice == "2":
                option_top_largest(df)
            elif choice == "3":
                option_top_smallest(df)
            elif choice == "4":
                option_compare_oecd(df)
            elif choice == "5":
                option_plot(df)
            elif choice == "0":
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please try again.")

    except FileNotFoundError:
        print("❌ Error: CSV file not found. Make sure it's in the same directory as this script.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
