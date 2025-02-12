import pandas as pd
import logging
import os

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def transform_naivas_data(file_path):
    """Transform Naivas dataset into long format with correct QTY and totalsales alignment."""
    # Load the data
    df = pd.read_csv(file_path)
    
    # Define the store columns for QTY and totalsales
    store_columns = [
        "CAPITAL CENTER", "GATEWAY MALL-SYOKIMAU", "MALINDI", "WESTLANDS", "BAMBURI", "KAHAWA SUKARI",
        "PRESTIGE", "MWEMBE TAYARI", "GREENSPAN", "UKUNDA", "SOUTH C", "UTAWALA", "MOUNTAIN VIEW",
        "NYALI BAZAAR", "IMARA DAIMA", "KITENGELA", "KILIMANI", "KILIFI", "LIKONI", "RUAI", "BURUBURU",
        "T SQUARE BURUBURU", "KINGARA ROAD", "MAIYAN MALL RONGAI", "MOI AVENUE", "ELGON VIEW ELDORET",
        "NYALI", "KATANI ROAD", "NYERI", "JUJA CITY", "EASTERN BYPASS", "EMBAKASI NYAYO",
        "NAKURU SUPERCENTER", "WATERFRONT KAREN", "NAIROBI WEST", "LANGATA MEDLINK", "KAKAMEGA",
        "NAKURU WESTSIDE", "THIKA TOWN", "MTWAPA", "LANGATA", "MOUNTAIN MALL", "ONESTOP KAREN",
        "MWANZI ROAD", "OJIJO RD", "RIRUTA", "KISII HYPER", "DEVELOPMENT HOUSE", "SPUR MALL",
        "EASTGATE", "BUNGOMA", "THIKA ANANAS", "WOODAVENUE KILIMANI", "MACHAKOS SUPERCENTRE",
        "KUBWA BRANCH", "SOKONI", "KISUMU SIMBA", "TUDOR MOMBASA", "LIFESTYLE CBD", "NAKURU MIDTOWN",
        "ZION MALL", "NGONG TOWN 2", "THINDIGUA", "KIAMBU ROAD", "RONALD NGALA", "NAKURU DOWNTOWN",
        "ELDORET REFERRAL", "SHELL SURVEY", "TILISI", "KISUMU", "HOMEGROUND", "EMBU PEARL CENTER",
        "LAVINGTON CURVE", "MALINDI HIGHWAY", "NAROK", "AIRPORT VIEW", "LIMURU", "AGA KHAN WALK",
        "KOMAROCK", "GREENHOUSE", "KISUMU MEGA CITY", "UMOJA", "MAVOKO", "BOMBOLULU", "KAPSABET",
        "GITHURAI 44", "GITHURAI", "EXPRESS EMBAKASI", "KIAMBU TOWN", "EMBU", "SAFARI CENTER",
        "HAZINA", "KISII", "KITUI", "KANGEMI", "JOGOO ROAD", "EXPRESS SHELL BARAKA", "MERU", "NDOGO",
        "RUARAKA", "SAIKA", "KAHAWA WEST", "KERICHO"
    ]

    # Create a list to hold all the transformed rows
    transformed_data = []

    # Iterate over each row in the original dataframe
    for _, row in df.iterrows():
        item_code = row['ITEMLOOKUPCODE']
        barcode = row['BARCODE']
        description = row['DESCRIPTION']
        category = row['CATEGORY']

        # Loop through each store and gather the corresponding QTY and totalsales
        for store in store_columns:
            qty_col = f'{store}_QTY'
            sales_col = f'{store}_totalsales'

            if qty_col in df.columns and sales_col in df.columns:
                qty = row[qty_col]
                sales = row[sales_col]

                # Only add a row if QTY is valid and greater than 0
                if pd.notna(qty) and qty > 0:
                    transformed_data.append({
                        'ITEMLOOKUPCODE': item_code,
                        'BARCODE': barcode,
                        'DESCRIPTION': description,
                        'CATEGORY': category,
                        'StoreName': store,
                        'QTY': qty,
                        'TotalSales': sales
                    })

    # Create a new DataFrame from the transformed data
    transformed_df = pd.DataFrame(transformed_data)

    # Define the output path
    output_dir = 'artifacts/naivas/edited_columns'
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

    # Save the transformed data
    output_path = os.path.join(output_dir, 'cleaned_data_transformed.csv')
    transformed_df.to_csv(output_path, index=False)
    logging.info(f"Data transformation completed and saved to {output_path}")

# Example usage
file_path = 'artifacts/naivas/formatted/flattened_data.csv'
transform_naivas_data(file_path)
