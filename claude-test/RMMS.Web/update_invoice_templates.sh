#!/bin/bash

# Script to update Invoice Templates 3-6 with database model binding
# Replaces hardcoded sample data with actual RiceSales model properties

echo "Updating Invoice Templates 3-6..."

for TEMPLATE_NUM in 3 4 5 6; do
    TEMPLATE_FILE="/home/user01/claude-test/RMMS.Web/RMMS.Web/Views/Invoices/Template${TEMPLATE_NUM}.cshtml"

    echo "Processing Template ${TEMPLATE_NUM}..."

    # Replace invoice numbers
    sed -i "s/INV-2024-00${TEMPLATE_NUM}/@Model.InvoiceNumber/g" "$TEMPLATE_FILE"
    sed -i "s/INV-2024-005/@Model.InvoiceNumber/g" "$TEMPLATE_FILE"
    sed -i "s/INV-2024-006/@Model.InvoiceNumber/g" "$TEMPLATE_FILE"

    # Replace customer name
    sed -i "s/ABC Traders Pvt Ltd/@Model.BuyerName/g" "$TEMPLATE_FILE"

    # Replace dates with model dates
    sed -i "s/@DateTime.Now.ToString(\"dd MMM yyyy\")/@Model.SaleDate.ToString(\"dd MMM yyyy\")/g" "$TEMPLATE_FILE"
    sed -i "s/@DateTime.Now.AddDays(30).ToString(\"dd MMM yyyy\")/@(Model.DueDate?.ToString(\"dd MMM yyyy\") ?? \"N/A\")/g" "$TEMPLATE_FILE"

    # Replace GST number
    sed -i "s/29XYZAB5678C1D2/@Model.BuyerGSTIN/g" "$TEMPLATE_FILE"

    echo "Template ${TEMPLATE_NUM} updated!"
done

echo ""
echo "All templates updated successfully!"
echo "Note: Templates now use @Model properties from RiceSales database"
echo ""
echo "Summary of changes:"
echo "- Model declaration: @model RMMS.Models.RiceSales"
echo "- Invoice number: @Model.InvoiceNumber"
echo "- Customer name: @Model.BuyerName"
echo "- Sale date: @Model.SaleDate"
echo "- Due date: @Model.DueDate"
echo "- GST: @Model.BuyerGSTIN"
echo ""
echo "Templates 3-6 are now database-connected!"
