#!/bin/bash

# Deployment script for Bracket Order Implementation
# Usage: bash deploy-bracket-orders.sh [branch-name] [environment]
# Example: bash deploy-bracket-orders.sh feature/bracket-orders production

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
GITHUB_USER="${GITHUB_USER:-code-python-in}"
REPO_NAME="${REPO_NAME:-openalgo}"
BRANCH_NAME="${1:-feature/bracket-orders}"
ENVIRONMENT="${2:-development}"
PROJECT_PATH="${PROJECT_PATH:-.}"

# Functions
print_header() {
    echo -e "\n${CYAN}$(printf '=%.0s' {1..80})${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}$(printf '=%.0s' {1..80})${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Main deployment script
main() {
    print_header "Bracket Order Deployment Script"

    echo "Configuration:"
    echo "  GitHub User: $GITHUB_USER"
    echo "  Repository: $REPO_NAME"
    echo "  Branch: $BRANCH_NAME"
    echo "  Environment: $ENVIRONMENT"
    echo "  Project Path: $PROJECT_PATH"
    echo ""

    # Step 1: Check prerequisites
    print_header "Step 1: Checking Prerequisites"

    # Check if Git is installed
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version)
        print_success "Git installed: $GIT_VERSION"
    else
        print_error "Git is not installed"
        exit 1
    fi

    # Check if Python is installed
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_success "Python installed: $PYTHON_VERSION"
    else
        print_error "Python 3 is not installed"
        exit 1
    fi

    # Check if pip is installed
    if command -v pip3 &> /dev/null; then
        PIP_VERSION=$(pip3 --version)
        print_success "pip installed: $PIP_VERSION"
    else
        print_error "pip is not installed"
        exit 1
    fi

    # Step 2: Clone or update repository
    print_header "Step 2: Cloning/Updating Repository"

    if [ -d "$PROJECT_PATH/.git" ]; then
        print_warning "Repository already exists at $PROJECT_PATH"
        echo "Pulling latest changes..."
        cd "$PROJECT_PATH"
        git fetch origin
        print_success "Repository updated"
    else
        echo "Cloning repository..."
        git clone --branch "$BRANCH_NAME" "https://github.com/$GITHUB_USER/$REPO_NAME.git" "$PROJECT_PATH"
        cd "$PROJECT_PATH"
        print_success "Repository cloned"
    fi

    # Step 3: Switch to correct branch
    print_header "Step 3: Switching to Branch"

    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
    if [ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]; then
        echo "Current branch: $CURRENT_BRANCH"
        echo "Switching to: $BRANCH_NAME"
        git checkout "$BRANCH_NAME"
        git pull origin "$BRANCH_NAME"
        print_success "Switched to branch: $BRANCH_NAME"
    else
        print_success "Already on branch: $BRANCH_NAME"
        git pull origin "$BRANCH_NAME"
    fi

    # Step 4: Install/update dependencies
    print_header "Step 4: Installing Dependencies"

    if [ -f "requirements.txt" ]; then
        echo "Installing packages from requirements.txt..."
        pip3 install -r requirements.txt
        print_success "Dependencies installed"
    else
        print_error "requirements.txt not found"
        exit 1
    fi

    # Step 5: Configure environment
    print_header "Step 5: Configuring Environment"

    if [ -f ".env" ]; then
        print_warning ".env file already exists"
        echo "Backing up to .env.backup"
        cp .env .env.backup
    fi

    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            echo "Creating .env from .env.example"
            cp .env.example .env
        else
            echo "Creating .env file"
            cat > .env << 'EOF'
# Bracket Order Configuration
BRACKET_ORDER_RATE_LIMIT=2 per second
BRACKET_ORDER_DELAY=0.5

# Flask Configuration
FLASK_ENV=production
DEBUG=False
EOF
        fi

        print_success ".env file created"
    fi

    # Step 6: Verify files
    print_header "Step 6: Verifying Implementation Files"

    FILES_TO_CHECK=(
        "services/bracket_order_service.py"
        "restx_api/bracket_order.py"
        "blueprints/tv_json.py"
        "restx_api/__init__.py"
    )

    ALL_FILES_EXIST=true
    for file in "${FILES_TO_CHECK[@]}"; do
        if [ -f "$file" ]; then
            print_success "Found: $file"
        else
            print_error "Missing: $file"
            ALL_FILES_EXIST=false
        fi
    done

    if [ "$ALL_FILES_EXIST" = false ]; then
        print_error "Some required files are missing"
        exit 1
    fi

    # Step 7: Run tests (if applicable)
    print_header "Step 7: Running Tests"

    if [ -d "test" ] && [ -f "test/conftest.py" ]; then
        echo "Running pytest..."
        python3 -m pytest test/ -v
        print_success "Tests passed"
    else
        print_warning "No tests found"
    fi

    # Step 8: Database initialization
    print_header "Step 8: Database Initialization"

    if [ -f "database/db_init_helper.py" ]; then
        echo "Initializing database..."
        python3 -c "from database.apilog_db import init_db; init_db()"
        print_success "Database initialized"
    else
        print_warning "Database initialization script not found"
    fi

    # Step 9: Deployment summary
    print_header "Deployment Summary"

    echo "Deployment completed successfully!"
    echo ""
    echo "Next steps:"
    echo ""

    if [ "$ENVIRONMENT" = "production" ]; then
        cat << 'EOF'
For Production Deployment:

1. Restart Flask application:
   systemctl restart openalgo
   # or for Docker:
   docker-compose restart openalgo

2. Verify application is running:
   systemctl status openalgo
   # or
   curl http://localhost:5000/health

3. Test bracket order endpoints:
   curl -X POST http://localhost:5000/api/v1/placebracketorder/ \
     -H "Content-Type: application/json" \
     -d '{
       "apikey": "YOUR_API_KEY",
       "symbol": "INFY",
       "exchange": "NSE",
       "product": "MIS",
       "action": "BUY",
       "quantity": 1,
       "entry_price": 1500,
       "sl_price": 1480,
       "target_price": 1550
     }'

4. Check logs:
   tail -f logs/openalgo.log

5. Monitor database:
   sqlite3 db/openalgo.db "SELECT * FROM order_logs WHERE api_type='placebracketorder' LIMIT 5;"
EOF
    else
        cat << 'EOF'
For Development/Testing:

1. Start Flask development server:
   python3 app.py
   # or
   FLASK_ENV=development python3 -m flask run

2. Test bracket order endpoints:
   curl -X POST http://localhost:5000/api/v1/placebracketorder/ \
     -H "Content-Type: application/json" \
     -d '{
       "apikey": "YOUR_API_KEY",
       "symbol": "INFY",
       "exchange": "NSE",
       "product": "MIS",
       "action": "BUY",
       "quantity": 1,
       "entry_price": 1500,
       "sl_price": 1480,
       "target_price": 1550
     }'

3. Check logs:
   tail -f logs/openalgo.log

4. Access API documentation:
   http://localhost:5000/api/v1/

5. Test webhook (TradingView):
   curl -X POST http://localhost:5000/tradingview/webhook/bracket \
     -H "Content-Type: application/json" \
     -d '{ ... }'
EOF
    fi

    echo ""
    echo "Documentation:"
    echo "  - BRACKET_ORDER_README.md (Quick start)"
    echo "  - BRACKET_ORDER_QUICK_REFERENCE.md (Reference)"
    echo "  - BRACKET_ORDER_DEPLOYMENT_SUMMARY.md (Detailed deployment)"
    echo "  - GITHUB_PUSH_AND_DEPLOY_GUIDE.md (GitHub guide)"
    echo ""

    print_success "Deployment ready!"
}

# Run main function
main "$@"

