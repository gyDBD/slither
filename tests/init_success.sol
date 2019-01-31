
contract C{
  address public owner;
  bool aa = false;

  event OwnershipRenounced(address indexed previousOwner);
  event OwnershipTransferred(
    address indexed previousOwner,
    address indexed newOwner
  );


  /**
   * @dev The Ownable constructor sets the original `owner` of the contract to the sender
   * account.
   */
  constructor() public {
    owner = msg.sender;
  }

  /**
   * @dev Throws if called by any account other than the owner.
   */
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }
  function onlyAdmin(bool forObserver) internal view {
    require(msg.sender == owner || forObserver==true);
  }
  function turn() internal view {
    require(msg.sender == owner);
  }
  function out() public {
    i_am_a_Initialize(true);
  }

  function i_am_a_Initialize(bool parameter) private {
    require(!aa)
    aa = parameter;
  }

}
