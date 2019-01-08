// These tests were made to ensure no false-positives as a result of state variable usage in inheriting/base contracts.
// The names should indicate whether or not they should be constant. Some are already marked constant.

contract A {

    address constant public alreadyConstAddr = 0xE0f5206BBD039e7b0592d8918820024e2a7437b9;
    address public constAddr1 = 0xc0ffee254729296a45a3885639AC7E10F9d54979;

    uint public used;
    uint public usedThroughInheritance = 7;
    uint public usedThroughInheritance2 = 7;
    uint public constUIntShadowed = 5;

    uint constant X = 32**22 + 8;
    string constant alreadyConstant = "abc";
    string constStr1 = "xyz";

    function setUsed() public {
        if (msg.sender == alreadyConstAddr) {
            used = constUIntShadowed;
        }
    }
}


contract B is A {

    address public constAddr2 = 0x999999cf1046e68e36E1aA2E0E07105eDDD1f08E;
    uint public usedThroughInheritance3 = 7;

    function () external {
        used = 0;
    }

    function setUsed(uint a) public {
        if (msg.sender == alreadyConstAddr) {
            used = a;
            usedThroughInheritance += 1;
        }
    }
}

contract C is B {
    address public constAddr3 = 0x999999cf1046e68e36E1aA2E0E07105eDDD1f08E;
    uint public constUIntShadowed = 6;

    function setUsed(uint a) public {
        if (msg.sender == alreadyConstAddr) {
            used += 1;
            usedThroughInheritance2 += 1;
            usedThroughInheritance3 += 1;
        }
    }
}