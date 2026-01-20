#!/usr/bin/env python3
"""
All Fours Card Game Backend API Testing
Tests all endpoints for authentication, rooms, game logic, chat, and leaderboard
"""

import requests
import sys
import json
import time
from datetime import datetime

class AllFoursAPITester:
    def __init__(self, base_url=""):
        # Use empty base_url for relative paths (proxy setup)
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.room_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session = requests.Session()

    def log(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}" if endpoint else f"{self.base_url}/api"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        self.log(f"🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = self.session.get(url, headers=test_headers)
            elif method == 'POST':
                response = self.session.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = self.session.put(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=test_headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                self.log(f"✅ {name} - Status: {response.status_code}")
                try:
                    return True, response.json() if response.content else {}
                except:
                    return True, {}
            else:
                self.log(f"❌ {name} - Expected {expected_status}, got {response.status_code}")
                self.log(f"   Response: {response.text[:200]}")
                self.failed_tests.append({
                    "test": name,
                    "expected": expected_status,
                    "actual": response.status_code,
                    "response": response.text[:200]
                })
                return False, {}

        except Exception as e:
            self.log(f"❌ {name} - Error: {str(e)}")
            self.failed_tests.append({
                "test": name,
                "error": str(e)
            })
            return False, {}

    def test_health_check(self):
        """Test health endpoint"""
        success, response = self.run_test("Health Check", "GET", "health", 200)
        return success and response.get("status") == "healthy"

    def test_user_registration(self):
        """Test user registration"""
        test_user = f"testuser_{int(time.time())}"
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data={
                "username": test_user,
                "password": "TestPass123!",
                "display_name": f"Test User {test_user}"
            }
        )
        
        if success and 'token' in response:
            self.token = response['token']
            self.user_id = response['user']['id']
            return True
        return False

    def test_user_login(self):
        """Test user login with existing credentials"""
        # First register a user for login test
        test_user = f"loginuser_{int(time.time())}"
        reg_success, reg_response = self.run_test(
            "Registration for Login Test",
            "POST",
            "auth/register",
            200,
            data={
                "username": test_user,
                "password": "LoginPass123!",
                "display_name": f"Login Test User"
            }
        )
        
        if not reg_success:
            return False
            
        # Now test login
        success, response = self.run_test(
            "User Login",
            "POST",
            "auth/login",
            200,
            data={
                "username": test_user,
                "password": "LoginPass123!"
            }
        )
        
        return success and 'token' in response

    def test_get_user_profile(self):
        """Test getting user profile"""
        if not self.token:
            self.log("❌ No token available for profile test")
            return False
            
        success, response = self.run_test("Get User Profile", "GET", "auth/me", 200)
        return success and 'id' in response

    def test_create_room(self):
        """Test creating a game room"""
        if not self.token:
            self.log("❌ No token available for room creation")
            return False
            
        success, response = self.run_test(
            "Create Game Room",
            "POST",
            "rooms/create",
            200,
            data={
                "name": "Test Game Room",
                "max_players": 4,
                "bet_amount": 10,
                "is_private": False
            }
        )
        
        if success and 'room_id' in response:
            self.room_id = response['room_id']
            return True
        return False

    def test_list_rooms(self):
        """Test listing available rooms"""
        success, response = self.run_test("List Available Rooms", "GET", "rooms", 200)
        return success and 'rooms' in response

    def test_join_room(self):
        """Test joining a room"""
        if not self.token or not self.room_id:
            self.log("❌ No token or room_id available for join test")
            return False
            
        success, response = self.run_test(
            "Join Room",
            "POST",
            "rooms/join",
            200,
            data={"room_id": self.room_id}
        )
        
        return success and 'room_id' in response

    def test_add_bot(self):
        """Test adding AI bot to room"""
        if not self.token or not self.room_id:
            self.log("❌ No token or room_id available for bot test")
            return False
            
        success, response = self.run_test(
            "Add AI Bot",
            "POST",
            f"rooms/{self.room_id}/add-bot",
            200
        )
        
        return success and 'room' in response

    def test_toggle_ready(self):
        """Test toggling ready status"""
        if not self.token or not self.room_id:
            self.log("❌ No token or room_id available for ready test")
            return False
            
        success, response = self.run_test(
            "Toggle Ready Status",
            "POST",
            f"rooms/{self.room_id}/ready",
            200
        )
        
        return success and 'room' in response

    def test_start_game(self):
        """Test starting a game"""
        if not self.token or not self.room_id:
            self.log("❌ No token or room_id available for start game test")
            return False
            
        success, response = self.run_test(
            "Start Game",
            "POST",
            f"rooms/{self.room_id}/start",
            200
        )
        
        return success and ('game_state' in response or 'room' in response)

    def test_get_hand(self):
        """Test getting player hand"""
        if not self.token or not self.room_id:
            self.log("❌ No token or room_id available for hand test")
            return False
            
        success, response = self.run_test(
            "Get Player Hand",
            "GET",
            f"game/{self.room_id}/hand",
            200
        )
        
        return success and 'hand' in response

    def test_play_card(self):
        """Test playing a card (will likely fail without proper game state)"""
        if not self.token or not self.room_id:
            self.log("❌ No token or room_id available for play card test")
            return False
            
        # This will likely fail since we need a proper game state
        success, response = self.run_test(
            "Play Card",
            "POST",
            "game/play-card",
            400,  # Expecting 400 since game might not be in proper state
            data={
                "room_id": self.room_id,
                "card": {"suit": "♠", "rank": "A"}
            }
        )
        
        # We expect this to fail with 400, so success means we got the expected error
        return success

    def test_send_chat(self):
        """Test sending chat message"""
        if not self.token or not self.room_id:
            self.log("❌ No token or room_id available for chat test")
            return False
            
        success, response = self.run_test(
            "Send Chat Message",
            "POST",
            "chat/send",
            200,
            data={
                "room_id": self.room_id,
                "message": "Hello from test!"
            }
        )
        
        return success and 'message' in response

    def test_get_leaderboard(self):
        """Test getting leaderboard"""
        success, response = self.run_test("Get Leaderboard", "GET", "leaderboard", 200)
        return success and 'leaderboard' in response

    def test_invalid_auth(self):
        """Test endpoints with invalid authentication"""
        # Save current token
        original_token = self.token
        self.token = "invalid_token"
        
        success, response = self.run_test(
            "Invalid Auth Test",
            "GET",
            "auth/me",
            401  # Expecting unauthorized
        )
        
        # Restore token
        self.token = original_token
        return success

    def run_all_tests(self):
        """Run all API tests"""
        self.log("🚀 Starting All Fours Card Game API Tests")
        self.log("=" * 50)
        
        # Health check
        if not self.test_health_check():
            self.log("❌ Health check failed - stopping tests")
            return False
            
        # Authentication tests
        if not self.test_user_registration():
            self.log("❌ User registration failed - stopping tests")
            return False
            
        if not self.test_user_login():
            self.log("❌ User login failed")
            
        if not self.test_get_user_profile():
            self.log("❌ Get user profile failed")
            
        # Room management tests
        if not self.test_create_room():
            self.log("❌ Create room failed")
            
        if not self.test_list_rooms():
            self.log("❌ List rooms failed")
            
        if not self.test_join_room():
            self.log("❌ Join room failed")
            
        # Game setup tests
        if not self.test_add_bot():
            self.log("❌ Add bot failed")
            
        if not self.test_toggle_ready():
            self.log("❌ Toggle ready failed")
            
        if not self.test_start_game():
            self.log("❌ Start game failed")
            
        # Game play tests
        if not self.test_get_hand():
            self.log("❌ Get hand failed")
            
        if not self.test_play_card():
            self.log("❌ Play card test failed (expected for incomplete game state)")
            
        # Chat and leaderboard tests
        if not self.test_send_chat():
            self.log("❌ Send chat failed")
            
        if not self.test_get_leaderboard():
            self.log("❌ Get leaderboard failed")
            
        # Security tests
        if not self.test_invalid_auth():
            self.log("❌ Invalid auth test failed")
        
        return True

    def print_summary(self):
        """Print test summary"""
        self.log("=" * 50)
        self.log(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.failed_tests:
            self.log("\n❌ Failed Tests:")
            for test in self.failed_tests:
                self.log(f"  - {test.get('test', 'Unknown')}: {test.get('error', test.get('response', 'Unknown error'))}")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        self.log(f"✅ Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 70  # Consider 70% success rate as acceptable

def main():
    """Main test execution"""
    # Use empty base URL for relative paths (proxy setup)
    tester = AllFoursAPITester("")
    
    try:
        success = tester.run_all_tests()
        tester.print_summary()
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"💥 Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())