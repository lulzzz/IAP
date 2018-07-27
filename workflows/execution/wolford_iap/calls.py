import sys
import os

# Navigate to Django root folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(sys.path[0]))))

# from workflows.transformations.projects.wolford_iap import consolidated_plan


def generate_consolidated_plan(dim_iapfilter, file_path_abs):
    r"""
    Generate the consolidated plan
    """
    # Generate plan
    # consolidated_plan.run(dim_iapfilter)
    # print('Consolidation completed')
    #
    # # Export to Excel
    # consolidated_plan.export_to_excel(dim_iapfilter, file_path_abs)
    # print('Export to Excel completed')

    return True
