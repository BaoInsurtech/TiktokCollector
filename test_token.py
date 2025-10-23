import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db.client import connect_db, disconnect_db, get_access_token_by_id

async def test_get_token():
    """Test lấy token với customer_id=1"""
    print("=" * 60)
    print("🧪 Testing get_access_token_by_id(customer_id=1)")
    print("=" * 60)
    
    try:
        # Connect database
        await connect_db()
        print("✅ Connected to database\n")
        
        # Test với customer_id=1
        print("📝 Fetching token for customer_id=1...")
        tokens = get_access_token_by_id(customer_id=1)  # ✅ Bỏ await vì function giờ là sync
        
        print(f"\n📊 Results:")
        print(f"   Found: {len(tokens)} token(s)")
        
        if tokens:
            token = tokens[0]
            print(f"\n✅ Token data:")
            print(f"   customer_id: {token.get('customer_id')}")
            print(f"   access_token: {token.get('access_token', 'N/A')[:30]}...")
            print(f"   refresh_token: {token.get('refresh_token', 'N/A')[:30]}...")
            print(f"   access_token_expire_in: {token.get('access_token_expire_in')}")
            print(f"   refresh_token_expire_in: {token.get('refresh_token_expire_in')}")
        else:
            print("\n⚠️ No token found for customer_id=1")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Disconnect
        await disconnect_db()
        print("\n✅ Disconnected from database")
    
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_get_token())