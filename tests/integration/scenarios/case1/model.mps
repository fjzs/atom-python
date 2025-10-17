*SENSE:Minimize
NAME          UFLP
ROWS
 N  Total_Costs
 E  AssignCustomer_0
 E  AssignCustomer_1
 L  OpenFacility_0_for_Customer_0
 L  OpenFacility_0_for_Customer_1
 L  OpenFacility_1_for_Customer_0
 L  OpenFacility_1_for_Customer_1
COLUMNS
    MARK      'MARKER'                 'INTORG'
    assign_facility_to_customer_(0,_0)  AssignCustomer_0   1.000000000000e+00
    assign_facility_to_customer_(0,_0)  OpenFacility_0_for_Customer_0   1.000000000000e+00
    assign_facility_to_customer_(0,_0)  Total_Costs   4.970000000000e+01
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    assign_facility_to_customer_(0,_1)  AssignCustomer_1   1.000000000000e+00
    assign_facility_to_customer_(0,_1)  OpenFacility_0_for_Customer_1   1.000000000000e+00
    assign_facility_to_customer_(0,_1)  Total_Costs   1.820000000000e+01
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    assign_facility_to_customer_(1,_0)  AssignCustomer_0   1.000000000000e+00
    assign_facility_to_customer_(1,_0)  OpenFacility_1_for_Customer_0   1.000000000000e+00
    assign_facility_to_customer_(1,_0)  Total_Costs   9.280000000000e+01
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    assign_facility_to_customer_(1,_1)  AssignCustomer_1   1.000000000000e+00
    assign_facility_to_customer_(1,_1)  OpenFacility_1_for_Customer_1   1.000000000000e+00
    assign_facility_to_customer_(1,_1)  Total_Costs   5.100000000000e+01
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    open_facility_0  OpenFacility_0_for_Customer_0  -1.000000000000e+00
    open_facility_0  OpenFacility_0_for_Customer_1  -1.000000000000e+00
    open_facility_0  Total_Costs   8.000000000000e+01
    MARK      'MARKER'                 'INTEND'
    MARK      'MARKER'                 'INTORG'
    open_facility_1  OpenFacility_1_for_Customer_0  -1.000000000000e+00
    open_facility_1  OpenFacility_1_for_Customer_1  -1.000000000000e+00
    open_facility_1  Total_Costs   9.000000000000e+01
    MARK      'MARKER'                 'INTEND'
RHS
    RHS       AssignCustomer_0   1.000000000000e+00
    RHS       AssignCustomer_1   1.000000000000e+00
    RHS       OpenFacility_0_for_Customer_0   0.000000000000e+00
    RHS       OpenFacility_0_for_Customer_1   0.000000000000e+00
    RHS       OpenFacility_1_for_Customer_0   0.000000000000e+00
    RHS       OpenFacility_1_for_Customer_1   0.000000000000e+00
BOUNDS
 BV BND       assign_facility_to_customer_(0,_0)
 BV BND       assign_facility_to_customer_(0,_1)
 BV BND       assign_facility_to_customer_(1,_0)
 BV BND       assign_facility_to_customer_(1,_1)
 BV BND       open_facility_0
 BV BND       open_facility_1
ENDATA
