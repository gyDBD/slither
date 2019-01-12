
contract C{

    function i_am_a_initialize() public{
        selfdestruct(msg.sender);
    }

}
