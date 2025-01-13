import logging
import sys

# Import the pipeline steps
from sleeklady.format_change_01 import main as format_change_step
from sleeklady.filtered_02 import main as filtering_step
from sleeklady.dropped_03 import main as drop_columns_step
from sleeklady.create_brands_04 import main as create_brands_step
from sleeklady.categories_05 import main as classify_products_step
from sleeklady.storenames_06 import main as resolve_store_names_step
from sleeklady.capitalized_07 import main as capitalize_data_step
from sleeklady.final_excel import main as save_to_excel_step

# Configure the logger for the main script
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)


def main():
    """Main function to orchestrate the data cleaning pipeline."""
    try:
        logger.info("Starting the data cleaning pipeline.")

        # Step 1: Format Change
        logger.info("Step 1: Format Change - Converting Excel sheets to CSV.")
        format_change_step()

        # Step 2: Filter Data
        logger.info("Step 2: Filter Data - Filtering data for ALKHEMY BRANDS.")
        filtering_step()

        # Step 3: Drop Columns
        logger.info("Step 3: Drop Columns - Removing unnecessary columns.")
        drop_columns_step()

        # Step 4: Create Brands Column
        logger.info("Step 4: Create Brands Column - Adding 'Brands' column to the data.")
        create_brands_step()

        # Step 5: Classify Products
        logger.info("Step 5: Classify Products - Categorizing products using regex patterns.")
        classify_products_step()

        # Step 6: Resolve Store Names
        logger.info("Step 6: Resolve Store Names - Replacing store IDs with store names.")
        resolve_store_names_step()

        # Step 7: Capitalize Data
        logger.info("Step 7: Capitalize Data - Capitalizing all string data.")
        capitalize_data_step()

        # Step 8: Save to Excel
        logger.info("Step 8: Save to Excel - Saving the final transformed data to an Excel file.")
        save_to_excel_step()

        logger.info("Pipeline executed successfully.")

    except Exception as e:
        logger.error(f"An error occurred in the pipeline: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
