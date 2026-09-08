"""
Tests for ByteBreaker Core
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import Config, ScannerConfig, ExploitConfig
from core.authorization import AuthorizationManager
from core.logger import ByteBreakerLogger


class TestConfig:
    """Test configuration module"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = Config()
        assert config.scanner.timeout == 5
        assert config.scanner.max_threads == 50
        assert config.exploit.safe_mode == True
        assert config.cracker.hash_types == ["md5", "sha1", "sha256"]
    
    def test_config_validation(self):
        """Test configuration validation"""
        config = Config()
        assert config.validate_config() == True
        
        # Test invalid config
        config.scanner.max_threads = 1000
        assert config.validate_config() == False
    
    def test_config_save_load(self, tmp_path):
        """Test configuration save and load"""
        config = Config()
        config.config_file = str(tmp_path / "test_config.json")
        config.save_config()
        
        # Load saved config
        loaded_config = Config(str(tmp_path / "test_config.json"))
        assert loaded_config.scanner.timeout == config.scanner.timeout


class TestAuthorization:
    """Test authorization module"""
    
    def test_add_authorization(self, tmp_path):
        """Test adding authorization"""
        auth_manager = AuthorizationManager(str(tmp_path / "auth.json"))
        
        success = auth_manager.add_authorization(
            "example.com",
            ["recon", "scan"],
            "Test User",
            30
        )
        assert success == True
    
    def test_check_authorization(self, tmp_path):
        """Test checking authorization"""
        auth_manager = AuthorizationManager(str(tmp_path / "auth.json"))
        
        # Add authorization
        auth_manager.add_authorization(
            "example.com",
            ["recon", "scan"],
            "Test User",
            30
        )
        
        # Check valid authorization
        assert auth_manager.check_authorization("example.com", "recon") == True
        
        # Check invalid action
        assert auth_manager.check_authorization("example.com", "exploit") == False
        
        # Check unauthorized target
        assert auth_manager.check_authorization("other.com", "recon") == False
    
    def test_revoke_authorization(self, tmp_path):
        """Test revoking authorization"""
        auth_manager = AuthorizationManager(str(tmp_path / "auth.json"))
        
        # Add and revoke
        auth_manager.add_authorization("example.com", ["recon"], "Test User", 30)
        assert auth_manager.revoke_authorization("example.com") == True
        
        # Check revoked authorization
        assert auth_manager.check_authorization("example.com", "recon") == False


class TestLogger:
    """Test logger module"""
    
    def test_logger_creation(self, tmp_path):
        """Test logger creation"""
        logger = ByteBreakerLogger("TestLogger", str(tmp_path))
        assert logger.logger.name == "TestLogger"
    
    def test_logging_methods(self, tmp_path):
        """Test logging methods"""
        logger = ByteBreakerLogger("TestLogger", str(tmp_path))
        
        # Test all logging levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
        # Check log files exist
        assert (tmp_path / "bytebreaker.log").exists()
        assert (tmp_path / "errors.log").exists()
        assert (tmp_path / "bytebreaker.json").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
