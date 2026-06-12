#!/bin/bash
# Quantum AI - Supabase Setup Script

echo "🔧 Quantum AI - Supabase Setup"
echo "==============================="
echo ""

# Check if supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI not found. Please install it first:"
    echo "   https://github.com/supabase/cli"
    exit 1
fi

# Check if logged in
echo "📋 Checking Supabase login status..."
supabase projects list &> /dev/null
if [ $? -ne 0 ]; then
    echo "❌ Not logged in to Supabase. Run: supabase login"
    exit 1
fi

# Link to project
echo "🔗 Linking to Supabase project..."
supabase link --project-ref hiukihnkaowdztjwaoko
if [ $? -ne 0 ]; then
    echo "⚠️ Could not link to project. You may need to run manually:"
    echo "   supabase link --project-ref hiukihnkaowdztjwaoko"
fi

# Push database schema
echo "📊 Pushing database schema..."
supabase db push
if [ $? -eq 0 ]; then
    echo "✅ Database schema pushed successfully!"
else
    echo "⚠️ Schema push failed. You may need to run the SQL manually in Supabase dashboard."
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your API keys to quantum/backend/.env"
echo "2. Run the backend: cd quantum/backend && python app.py"
echo "3. Run the frontend: cd quantum/frontend && python -m http.server 3000"