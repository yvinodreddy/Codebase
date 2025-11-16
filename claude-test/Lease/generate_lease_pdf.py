#!/usr/bin/env python3
"""
Generate Professional Lease Agreement PDF
"""
import sys
import os

# Try to import reportlab, if not available, use a simpler approach
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("ReportLab not installed. Creating a text-based lease agreement instead.")

def create_pdf_with_reportlab():
    """Create PDF using ReportLab"""
    doc = SimpleDocTemplate(
        "/home/user01/claude-test/Lease/Lease_Agreement_Pagan_Lopez.pdf",
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=12
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )

    clause_style = ParagraphStyle(
        'ClauseStyle',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        firstLineIndent=0
    )

    # Title and Header
    elements.append(Paragraph("<b>RESIDENTIAL LEASE AGREEMENT</b>", title_style))
    elements.append(Paragraph("<b>NEW JERSEY STANDARD FORM</b>", heading_style))
    elements.append(Spacer(1, 12))

    # Warning Box
    warning_text = """<b>THIS IS A LEGALLY BINDING LEASE THAT WILL BECOME FINAL WITHIN THREE BUSINESS DAYS.
    DURING THIS PERIOD YOU MAY CHOOSE TO CONSULT AN ATTORNEY WHO CAN REVIEW AND CANCEL
    THE LEASE. SEE SECTION ON ATTORNEY REVIEW FOR DETAILS.</b>"""
    elements.append(Paragraph(warning_text, heading_style))
    elements.append(Spacer(1, 24))

    # Agreement Title
    elements.append(Paragraph("<b>RESIDENTIAL LEASE AGREEMENT</b>", title_style))
    elements.append(Spacer(1, 12))

    # Parties
    elements.append(Paragraph("<b>BETWEEN LANDLORD:</b> Wilfredo Pagan", normal_style))
    elements.append(Paragraph("<b>whose address is:</b> 39 Mansfield Road, Piscataway, NJ 08854", normal_style))
    elements.append(Paragraph("<b>Phone:</b> 732-900-5391", normal_style))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("<b>AND TENANT:</b> Levi Lopez", normal_style))
    elements.append(Paragraph("<b>whose address is:</b> 39 Mansfield Road, Piscataway, NJ 08854", normal_style))
    elements.append(Paragraph("<b>Phone:</b> 908-420-6457", normal_style))
    elements.append(Spacer(1, 12))

    # Definitions
    elements.append(Paragraph(
        'The word "Landlord" as used in this Lease means all of the landlords above listed. In all instances in which the Landlord may exercise rights or perform obligations under this Lease, it may do so through its authorized agents or representatives.',
        normal_style
    ))
    elements.append(Paragraph('The word "Tenant" as used in this Lease means all of the tenants above listed.', normal_style))
    elements.append(Spacer(1, 12))

    # Clauses
    clauses = [
        ("1. CONDOMINIUM/CO-OPERATIVE RIGHT OF TERMINATION:",
         "THIS BUILDING IS BEING CONVERTED TO OR IS A CONDOMINIUM OR COOPERATIVE. YOUR TENANCY CAN BE TERMINATED UPON 60 DAYS NOTICE IF YOUR APARTMENT IS SOLD TO A BUYER WHO SEEKS TO PERSONALLY OCCUPY IT. IF YOU MOVE OUT AS A RESULT OF RECEIVING SUCH A NOTICE, AND THE LANDLORD ARBITRARILY FAILS TO COMPLETE THE SALE, THE LANDLORD SHALL BE LIABLE FOR TREBLE DAMAGES AND COURT COSTS."),

        ("2. PROPERTY:",
         "The Tenant agrees to lease from the Landlord and the Landlord agrees to lease to the Tenant (the single family home) Apartment # N/A (condominium unit # N/A) having a street address of 39 Mansfield Road located in Piscataway, NJ 08854, New Jersey (referred to as the \"Property\")."),

        ("3. TERM:",
         "The Term of this Lease is for 36 months (months/years) starting on May 24, 2025 and ending on May 24, 2028. This is referred to as the \"Term\". If the Landlord is unable to give possession of the Property to the Tenant on the first day of the Term, the Landlord shall not have any liability to the Tenant. However, the Tenant shall not be liable for the payment of rent until the Landlord gives possession of the Property to the Tenant."),

        ("4. RENT:",
         "The rent for the Term of this Lease is $600.00 per month, to be paid as follows: $600.00 per month, which is due on the 1st day of each month. Rent shall be payable to: Wilfredo Pagan at the above address."),

        ("5. INITIAL DEPOSIT:",
         "Tenant has paid an initial deposit of $600.00 received on May 24, 2025 that will be credited towards the Security Deposit. The balance shall be paid as follows: First month's rent $600.00 Due on May 24, 2025, Security Deposit $600.00 Due on May 24, 2025."),

        ("6. SECURITY DEPOSIT:",
         "Tenant shall pay to the Landlord the sum of $600.00 (the \"Security Deposit\" which cannot exceed one and one-half month's rent) to assure that Tenant performs all of Tenant's obligations under this Lease. Landlord shall comply with the Rent Security Deposit Act (N.J.S.A. 46:8-19 et seq.)."),

        ("7. LATE PAYMENT PENALTY:",
         "If the Tenant does not pay the rent by the 5th day of the month, the Tenant shall pay a late charge of $50.00 per day the rent is received by Landlord. The late charge shall be added to the rent, and shall be considered as additional rent."),

        ("8. ADDITIONAL RENT:",
         "Landlord may perform any obligations under this Lease which are Tenant's responsibility and which Tenant fails to perform. The cost to Landlord for such performance may be charged to TENANT as \"additional rent\" which shall be due and payable with the next installment of monthly rent."),

        ("9. POSSESSION AND USE:",
         "The Landlord shall give possession of the Property to the Tenant for the Term of this Lease except as otherwise provided in this Lease. The Tenant shall occupy the Property only as a private residence, and will not use the Property for any business, trade or profession."),

        ("10. UTILITIES:",
         "UTILITIES INCLUDED IN RENT - The Landlord shall provide and pay for the following utility services: Gas, Electric, Water, Heat, Sewer, General Trash Disposal. All utilities are included in the monthly rent of $600.00."),
    ]

    for title, content in clauses:
        elements.append(Paragraph(f"<b>{title}</b> {content}", clause_style))

    # Add page break
    elements.append(PageBreak())

    # Continue with more clauses
    more_clauses = [
        ("11. NO ASSIGNMENT OR SUBLETTING:",
         "The Tenant may not assign this Lease, sublet all or any part of the Property, or permit any other person to use the Property without the prior written permission of the Landlord. The Landlord may withhold such permission in Landlord's sole and absolute discretion."),

        ("12. VIOLATION, EVICTION AND RE-ENTRY:",
         "The Landlord reserves the right of re-entry. This means that if the Tenant violates the terms of this Lease, the Landlord may terminate this Lease and regain possession of the Property. This is done by a court proceeding known as an eviction."),

        ("13. DAMAGES:",
         "The Tenant is liable for all Landlord's damages caused by Tenant's breach of this Lease. Such damages may include loss of rent, the cost of preparing the Property for re-renting, brokerage commissions in finding a new tenant as a result of Tenant's eviction or Tenant moves out prior to the end of the Term as well as reasonable attorney's fees and court costs."),

        ("14. QUIET ENJOYMENT:",
         "The Tenant may occupy the Property without interference, subject to Tenant's compliance with the Terms of this Lease."),

        ("15. TENANT'S REPAIRS AND MAINTENANCE:",
         "The Tenant shall: (a) Pay for all repairs, replacements and damages caused by the act or neglect of the Tenant, (b) Keep and maintain the Property in a neat, clean, safe and sanitary condition, (c) Cut the grass and maintain the shrubbery, (d) Drive and park vehicles only in designated areas, if any, (e) Take good care of the Property and all equipment, fixtures, carpeting and appliances located in it."),

        ("16. LANDLORD REPAIRS:",
         "The Landlord shall make any necessary repairs and replacements to the vital facilities serving the Property, such as the heating, plumbing and electrical systems, within a reasonable time after notice by the Tenant."),

        ("17. ACCESS TO THE PROPERTY:",
         "The Landlord shall have access to the Property on reasonable notice to the Tenant in order to inspect, make necessary repairs, supply services, and show it to prospective buyers or tenants."),

        ("18. NO ALTERATIONS OR INSTALLATION OF EQUIPMENT:",
         "The Tenant may not alter or change the Property without first obtaining Landlord's written consent."),

        ("19. INSPECTION:",
         "If the municipality requires a continued use inspection or certificate of occupancy prior to occupancy, the Landlord shall be responsible for obtaining such inspections and certificates as well as making the necessary repairs."),

        ("20. INSURANCE:",
         "The Tenant shall be responsible for obtaining, at Tenant's own cost and expense, a tenant's insurance policy for the Tenant's furniture, furnishings, clothing and other personal property."),
    ]

    for title, content in more_clauses:
        elements.append(Paragraph(f"<b>{title}</b> {content}", clause_style))

    # Add another page break
    elements.append(PageBreak())

    # Final clauses
    final_clauses = [
        ("21. FIRE AND OTHER CASUALTY:",
         "Immediate notice shall be given by the Tenant to Landlord of any fire or other casualty which occurs at the Property."),

        ("22. LIABILITY OF LANDLORD AND TENANT:",
         "The Landlord is not legally responsible for any loss, injury or damage to any person or property unless such loss, injury or damage is directly caused by the Landlord's negligence."),

        ("23. PETS:",
         "No dogs, cats or other pets shall be permitted on the Property without the prior written consent of the Landlord."),

        ("24. NOTICES:",
         "All notices given under this Lease must be in writing in order to be effective."),

        ("25. NO WAIVER:",
         "The Landlord's failure to enforce any obligation of the Tenant contained in this Lease in any one instance shall not prevent the Landlord from enforcing the obligation at a later time."),

        ("26. SEVERABILITY:",
         "If any term or condition of this Lease is contrary to law, the remainder of the Lease shall be unaffected and shall continue to be binding upon the parties."),

        ("27. RENEWAL OF LEASE:",
         "The Tenant must be offered a renewal of this Lease by the Landlord, unless the Landlord has good cause not to do so under applicable law."),

        ("28. FURNITURE:",
         "If the Property is leased in furnished condition, or if the Landlord leaves personal property to be used by the Tenant, the Tenant shall maintain the furniture and furnishings in good condition and repair."),

        ("29. END OF TERM:",
         "At the end of the Term, the Tenant shall leave the Property clean, remove all of the Tenant's property, repair any damage, and return it with all keys to the Landlord in the same condition as it was at the beginning of the Term, except for normal wear and tear."),

        ("30. ASSOCIATION BYLAWS, RULES AND REGULATIONS:",
         "If Property is subject to any Association Bylaws and Rules and Regulations, Tenant agrees to comply with such Association Bylaws and Rules and Regulations including any amendments."),

        ("31. BINDING:",
         "This Lease is binding on the Landlord and the Tenant and all parties who lawfully succeed to their rights and responsibilities."),

        ("32. ENTIRE AGREEMENT:",
         "This Lease contains the entire agreement of the Landlord and Tenant. No representations have been made by the Landlord or its real estate broker or agents except as set forth in this Lease. This Lease can only be changed in writing by an agreement signed by both the Landlord and the Tenant."),
    ]

    for title, content in final_clauses:
        elements.append(Paragraph(f"<b>{title}</b> {content}", clause_style))

    # Special Terms
    elements.append(Spacer(1, 24))
    elements.append(Paragraph("<b>35. SPECIAL TERMS AND CONDITIONS:</b>", clause_style))
    elements.append(Paragraph("<b>KITCHEN ACCESS INCLUDED</b> - Tenant shall have full access to kitchen facilities.", normal_style))
    elements.append(Paragraph("<b>ALL UTILITIES INCLUDED IN RENT</b> - Landlord shall pay for all utilities including gas, electric, water, heat, sewer, and trash disposal as part of the monthly rent of $600.00.", normal_style))

    # Add page break before signatures
    elements.append(PageBreak())

    # Signature Section
    elements.append(Spacer(1, 36))
    elements.append(Paragraph("<b>WITNESS:</b>", title_style))
    elements.append(Spacer(1, 36))

    # Signature table
    sig_data = [
        ['_'*40, '_'*20],
        ['Landlord: Wilfredo Pagan', 'Date'],
        ['', ''],
        ['_'*40, '_'*20],
        ['Tenant: Levi Lopez', 'Date'],
    ]

    sig_table = Table(sig_data, colWidths=[3.5*inch, 2*inch])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(sig_table)

    elements.append(Spacer(1, 24))
    elements.append(Paragraph("<b>SIGN ABOVE ON THE LINES PROVIDED</b>", title_style))

    # Build PDF
    doc.build(elements)
    print("PDF created successfully: Lease_Agreement_Pagan_Lopez.pdf")

def create_text_based_lease():
    """Create a text-based lease agreement that can be converted to PDF"""
    lease_content = """
================================================================================
                        RESIDENTIAL LEASE AGREEMENT
                         NEW JERSEY STANDARD FORM
================================================================================

THIS IS A LEGALLY BINDING LEASE THAT WILL BECOME FINAL WITHIN THREE BUSINESS DAYS.
DURING THIS PERIOD YOU MAY CHOOSE TO CONSULT AN ATTORNEY WHO CAN REVIEW AND CANCEL
THE LEASE. SEE SECTION ON ATTORNEY REVIEW FOR DETAILS.

================================================================================
                        RESIDENTIAL LEASE AGREEMENT
================================================================================

BETWEEN LANDLORD: Wilfredo Pagan
whose address is: 39 Mansfield Road, Piscataway, NJ 08854
Phone: 732-900-5391

AND TENANT: Levi Lopez
whose address is: 39 Mansfield Road, Piscataway, NJ 08854
Phone: 908-420-6457

The word "Landlord" as used in this Lease means all of the landlords above listed.
In all instances in which the Landlord may exercise rights or perform obligations
under this Lease, it may do so through its authorized agents or representatives.

The word "Tenant" as used in this Lease means all of the tenants above listed.

1. CONDOMINIUM/CO-OPERATIVE RIGHT OF TERMINATION: THIS BUILDING IS BEING CONVERTED
TO OR IS A CONDOMINIUM OR COOPERATIVE. YOUR TENANCY CAN BE TERMINATED UPON 60 DAYS
NOTICE IF YOUR APARTMENT IS SOLD TO A BUYER WHO SEEKS TO PERSONALLY OCCUPY IT. IF
YOU MOVE OUT AS A RESULT OF RECEIVING SUCH A NOTICE, AND THE LANDLORD ARBITRARILY
FAILS TO COMPLETE THE SALE, THE LANDLORD SHALL BE LIABLE FOR TREBLE DAMAGES AND
COURT COSTS.

2. PROPERTY: The Tenant agrees to lease from the Landlord and the Landlord agrees
to lease to the Tenant (the single family home) Apartment # N/A (condominium unit
# N/A) having a street address of 39 Mansfield Road located in Piscataway,
NJ 08854, New Jersey (referred to as the "Property").

3. TERM: The Term of this Lease is for 36 months (months/years) starting on
May 24, 2025 and ending on May 24, 2028. This is referred to as the "Term".
If the Landlord is unable to give possession of the Property to the Tenant on
the first day of the Term, the Landlord shall not have any liability to the
Tenant. However, the Tenant shall not be liable for the payment of rent until
the Landlord gives possession of the Property to the Tenant.

4. RENT: The rent for the Term of this Lease is $600.00 per month, to be paid
as follows: $600.00 per month, which is due on the 1st day of each month.
Rent shall be payable to: Wilfredo Pagan at the above address.

5. INITIAL DEPOSIT: Tenant has paid an initial deposit of $600.00 received on
May 24, 2025 that will be credited towards the Security Deposit. The balance
shall be paid as follows: First month's rent $600.00 Due on May 24, 2025,
Security Deposit $600.00 Due on May 24, 2025.

6. SECURITY DEPOSIT: Tenant shall pay to the Landlord the sum of $600.00
(the "Security Deposit" which cannot exceed one and one-half month's rent) to
assure that Tenant performs all of Tenant's obligations under this Lease.
Landlord shall comply with the Rent Security Deposit Act (N.J.S.A. 46:8-19 et seq.).

7. LATE PAYMENT PENALTY: If the Tenant does not pay the rent by the 5th day of
the month, the Tenant shall pay a late charge of $50.00 per day the rent is
received by Landlord. The late charge shall be added to the rent, and shall be
considered as additional rent.

8. ADDITIONAL RENT: Landlord may perform any obligations under this Lease which
are Tenant's responsibility and which Tenant fails to perform. The cost to
Landlord for such performance may be charged to TENANT as "additional rent"
which shall be due and payable with the next installment of monthly rent.

9. POSSESSION AND USE: The Landlord shall give possession of the Property to the
Tenant for the Term of this Lease except as otherwise provided in this Lease.
The Tenant shall occupy the Property only as a private residence, and will not
use the Property for any business, trade or profession.

10. UTILITIES: UTILITIES INCLUDED IN RENT - The Landlord shall provide and pay
for the following utility services: Gas, Electric, Water, Heat, Sewer, General
Trash Disposal. All utilities are included in the monthly rent of $600.00.

11. NO ASSIGNMENT OR SUBLETTING: The Tenant may not assign this Lease, sublet
all or any part of the Property, or permit any other person to use the Property
without the prior written permission of the Landlord. The Landlord may withhold
such permission in Landlord's sole and absolute discretion.

12. VIOLATION, EVICTION AND RE-ENTRY: The Landlord reserves the right of re-entry.
This means that if the Tenant violates the terms of this Lease, the Landlord may
terminate this Lease and regain possession of the Property. This is done by a
court proceeding known as an eviction.

13. DAMAGES: The Tenant is liable for all Landlord's damages caused by Tenant's
breach of this Lease. Such damages may include loss of rent, the cost of preparing
the Property for re-renting, brokerage commissions in finding a new tenant as a
result of Tenant's eviction or Tenant moves out prior to the end of the Term as
well as reasonable attorney's fees and court costs.

14. QUIET ENJOYMENT: The Tenant may occupy the Property without interference,
subject to Tenant's compliance with the Terms of this Lease.

15. TENANT'S REPAIRS AND MAINTENANCE: The Tenant shall:
(a) Pay for all repairs, replacements and damages caused by the act or neglect
    of the Tenant
(b) Keep and maintain the Property in a neat, clean, safe and sanitary condition
(c) Cut the grass and maintain the shrubbery
(d) Drive and park vehicles only in designated areas, if any
(e) Take good care of the Property and all equipment, fixtures, carpeting and
    appliances located in it

16. LANDLORD REPAIRS: The Landlord shall make any necessary repairs and
replacements to the vital facilities serving the Property, such as the heating,
plumbing and electrical systems, within a reasonable time after notice by the Tenant.

17. ACCESS TO THE PROPERTY: The Landlord shall have access to the Property on
reasonable notice to the Tenant in order to inspect, make necessary repairs,
supply services, and show it to prospective buyers or tenants.

18. NO ALTERATIONS OR INSTALLATION OF EQUIPMENT: The Tenant may not alter or
change the Property without first obtaining Landlord's written consent.

19. INSPECTION: If the municipality requires a continued use inspection or
certificate of occupancy prior to occupancy, the Landlord shall be responsible
for obtaining such inspections and certificates as well as making the necessary repairs.

20. INSURANCE: The Tenant shall be responsible for obtaining, at Tenant's own
cost and expense, a tenant's insurance policy for the Tenant's furniture,
furnishings, clothing and other personal property.

21. FIRE AND OTHER CASUALTY: Immediate notice shall be given by the Tenant to
Landlord of any fire or other casualty which occurs at the Property.

22. LIABILITY OF LANDLORD AND TENANT: The Landlord is not legally responsible
for any loss, injury or damage to any person or property unless such loss,
injury or damage is directly caused by the Landlord's negligence.

23. PETS: No dogs, cats or other pets shall be permitted on the Property without
the prior written consent of the Landlord.

24. NOTICES: All notices given under this Lease must be in writing in order to
be effective.

25. NO WAIVER: The Landlord's failure to enforce any obligation of the Tenant
contained in this Lease in any one instance shall not prevent the Landlord from
enforcing the obligation at a later time.

26. SEVERABILITY: If any term or condition of this Lease is contrary to law,
the remainder of the Lease shall be unaffected and shall continue to be binding
upon the parties.

27. RENEWAL OF LEASE: The Tenant must be offered a renewal of this Lease by the
Landlord, unless the Landlord has good cause not to do so under applicable law.

28. FURNITURE: If the Property is leased in furnished condition, or if the
Landlord leaves personal property to be used by the Tenant, the Tenant shall
maintain the furniture and furnishings in good condition and repair.

29. END OF TERM: At the end of the Term, the Tenant shall leave the Property
clean, remove all of the Tenant's property, repair any damage, and return it
with all keys to the Landlord in the same condition as it was at the beginning
of the Term, except for normal wear and tear.

30. ASSOCIATION BYLAWS, RULES AND REGULATIONS: If Property is subject to any
Association Bylaws and Rules and Regulations, Tenant agrees to comply with such
Association Bylaws and Rules and Regulations including any amendments.

31. BINDING: This Lease is binding on the Landlord and the Tenant and all
parties who lawfully succeed to their rights and responsibilities.

32. ENTIRE AGREEMENT: This Lease contains the entire agreement of the Landlord
and Tenant. No representations have been made by the Landlord or its real estate
broker or agents except as set forth in this Lease. This Lease can only be
changed in writing by an agreement signed by both the Landlord and the Tenant.

33. ATTORNEY REVIEW CLAUSE:
(1) Study by Attorney.
The Tenant or the Landlord may choose to have an attorney study this Lease.
If an attorney is consulted, the attorney must complete his or her review of
the Lease within a three-day period. This Lease will be legally binding at the
end of this three-day period unless an attorney for the Tenant or the Landlord
reviews or disapproves of the Lease.

(2) Counting the Time.
You count the three days from the date of delivery of the signed Lease to the
Tenant and the Landlord. You do not count Saturdays, Sundays or legal holidays.
The Landlord may agree in writing to extend the three-day period for attorney review.

(3) Notice of Disapproval.
If an attorney for the Tenant or the Landlord reviews and disapproves of this
Lease, the attorney must notify the Broker(s) and the other party named in this
Lease within the three-day period. Otherwise this Lease will be legally binding
as written.

34. BROKER'S COMMISSION: The Broker's Commission is earned, due and payable upon
signing of a fully executed Lease Agreement and satisfaction of the Attorney
Review Period set forth in Section 33 of this Lease.

35. SPECIAL TERMS AND CONDITIONS:
KITCHEN ACCESS INCLUDED - Tenant shall have full access to kitchen facilities.
ALL UTILITIES INCLUDED IN RENT - Landlord shall pay for all utilities including
gas, electric, water, heat, sewer, and trash disposal as part of the monthly
rent of $600.00.

================================================================================
                              WITNESS SIGNATURES
================================================================================

______________________________________     _____________________
Landlord: Wilfredo Pagan                    Date


______________________________________     _____________________
Tenant: Levi Lopez                          Date


SIGN ABOVE ON THE LINES PROVIDED

================================================================================
"""

    # Save as text file
    with open("/home/user01/claude-test/Lease/Lease_Agreement_Pagan_Lopez.txt", "w") as f:
        f.write(lease_content)

    print("Text-based lease agreement created: Lease_Agreement_Pagan_Lopez.txt")
    print("\nTo convert this to PDF, you can:")
    print("1. Open the HTML file (lease_agreement.html) in a web browser and print to PDF")
    print("2. Use the text file and format it in a word processor")
    print("3. Install reportlab: pip install reportlab")

if __name__ == "__main__":
    if REPORTLAB_AVAILABLE:
        create_pdf_with_reportlab()
    else:
        create_text_based_lease()
        print("\nHTML version is also available at: lease_agreement.html")
        print("You can open this file in a web browser and print it to PDF.")