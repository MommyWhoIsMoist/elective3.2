import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def clean_earnings_columns(df):
    earnings_columns = ["Total_Earnings", "Men_Earnings", "Women_Earnings"]
    for col in earnings_columns:
        df = df[~df[col].astype(str).str.contains('Median weekly earnings', na=False)]
        df[col] = (
            df[col]
            .replace({'–': np.nan, '': np.nan})
            .replace(r'[\$,]', '', regex=True)
            .apply(pd.to_numeric, errors='coerce')
        )
    return df

def load_and_clean_data():
    df = pd.read_csv("data/cpsaat39.csv", skiprows=7, header=None)
    df.columns = [
        "Occupation", 
        "Total_Workers", 
        "Total_Earnings", 
        "Men_Workers", 
        "Men_Earnings", 
        "Women_Workers", 
        "Women_Earnings"
    ]
    df = clean_earnings_columns(df)
    
    # Clean worker columns
    worker_columns = ["Total_Workers", "Men_Workers", "Women_Workers"]
    for col in worker_columns:
        df[col] = (
            df[col]
            .replace({'–': np.nan, '': np.nan})
            .replace(r'[\$,]', '', regex=True)
            .apply(pd.to_numeric, errors='coerce')
        )
    
    # Add Gender Pay Gap column
    df["Gender_Pay_Gap"] = df["Men_Earnings"] - df["Women_Earnings"]

    return df

def display_menu():
    print("\n📊 Select an option:")
    print("1 - Toggle earnings sort (High ↔ Low)")
    print("2 - Top 10 occupations with most women workers")
    print("3 - Top 10 occupations with most men workers")
    print("4 - Gender pay gap analysis")
    print("5 - Show bar chart of top 10 earnings by gender (toggle)")
    print("0 - Exit")

def option_sort_earnings(df, ascending):
    sorted_df = (
        df.sort_values(by="Total_Earnings", ascending=ascending)
        .dropna(subset=["Total_Earnings"])
        .head(10)
    )

    print(f"\nTop 10 occupations by total earnings ({'Lowest' if ascending else 'Highest'} first):")
    print(sorted_df[["Occupation", "Total_Earnings"]])

    return not ascending  # Toggle for next call

def option_top_women(df):
    top = df.sort_values(by="Women_Workers", ascending=False).dropna(subset=["Women_Workers"])
    print("\nTop 10 occupations with most women workers:")
    print(top[["Occupation", "Women_Workers"]].head(10))

def option_top_men(df):
    top = df.sort_values(by="Men_Workers", ascending=False).dropna(subset=["Men_Workers"])
    print("\nTop 10 occupations with most men workers:")
    print(top[["Occupation", "Men_Workers"]].head(10))

def option_gender_gap(df):
    gap_sorted = df.sort_values(by="Gender_Pay_Gap", ascending=False)
    print("\nTop 10 occupations where men earn more than women:")
    print(gap_sorted[["Occupation", "Men_Earnings", "Women_Earnings", "Gender_Pay_Gap"]].head(10))

    reverse_gap = gap_sorted[gap_sorted["Gender_Pay_Gap"] < 0]
    if not reverse_gap.empty:
        print("\nTop occupations where women earn more than men:")
        print(reverse_gap[["Occupation", "Men_Earnings", "Women_Earnings", "Gender_Pay_Gap"]].head(10))
    else:
        print("\nNo occupations found where women earn more than men.")

def option_plot_gender_toggle(df):
    gender_col = "Men_Earnings"
    while True:
        gender = "Men" if gender_col == "Men_Earnings" else "Women"
        top_10 = df.sort_values(by=gender_col, ascending=False).dropna(subset=[gender_col]).head(10)

        plt.figure(figsize=(10, 6))
        sns.barplot(data=top_10, x=gender_col, y="Occupation", palette="coolwarm")
        plt.title(f"Top 10 Highest Median Weekly Earnings ({gender})")
        plt.xlabel("Median Weekly Earnings ($)")
        plt.ylabel("Occupation")
        plt.tight_layout()
        plt.show()

        toggle = input("Press [T] to toggle gender or [M] to return to the main menu: ").strip().lower()
        if toggle == 't':
            gender_col = "Women_Earnings" if gender_col == "Men_Earnings" else "Men_Earnings"
        elif toggle == 'm':
            break
        else:
            print("Invalid input.")

def main():
    print("\n=== Running Dataset 1 Analysis ===")
    try:
        df = load_and_clean_data()
        ascending = False  # Initial sort order for earnings

        while True:
            display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                ascending = option_sort_earnings(df, ascending)
            elif choice == "2":
                option_top_women(df)
            elif choice == "3":
                option_top_men(df)
            elif choice == "4":
                option_gender_gap(df)
            elif choice == "5":
                option_plot_gender_toggle(df)
            elif choice == "0":
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please select a valid option.")

    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
