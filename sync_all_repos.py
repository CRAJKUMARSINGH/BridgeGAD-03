#!/usr/bin/env python3
"""
BridgeGAD Repository Synchronization Script
Synchronizes all local and remote repositories for all BridgeGAD applications
"""

import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def is_git_repo(path):
    """Check if directory is a git repository"""
    return (Path(path) / '.git').exists()

def run_git_command(command, cwd, timeout=60):
    """Run a git command in the specified directory"""
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, 
                              text=True, timeout=timeout, shell=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timeout"
    except Exception as e:
        return False, "", str(e)

def sync_repository(repo_path):
    """Synchronize a single repository"""
    repo_name = repo_path.name
    print(f"\\nSynchronizing {repo_name}...")
    
    if not is_git_repo(repo_path):
        print(f"  ⚠️  {repo_name} is not a git repository")
        
        # Initialize git repository if not exists
        print(f"  📦 Initializing git repository for {repo_name}")
        success, stdout, stderr = run_git_command("git init", repo_path)
        if not success:
            print(f"  ❌ Failed to initialize git: {stderr}")
            return False
        
        # Add all files
        success, stdout, stderr = run_git_command("git add .", repo_path)
        if not success:
            print(f"  ❌ Failed to add files: {stderr}")
            return False
        
        # Initial commit
        commit_message = f"Initial commit for {repo_name}"
        success, stdout, stderr = run_git_command(f'git commit -m "{commit_message}"', repo_path)
        if not success:
            print(f"  ⚠️  Commit may have failed (possibly nothing to commit): {stderr}")
        
        print(f"  ✅ {repo_name} initialized as git repository")
        return True
    
    print(f"  📂 {repo_name} is already a git repository")
    
    # Check git status
    success, stdout, stderr = run_git_command("git status --porcelain", repo_path)
    if not success:
        print(f"  ❌ Failed to get git status: {stderr}")
        return False
    
    changes = stdout.strip()
    if changes:
        print(f"  📝 Found {len(changes.splitlines())} changes")
        
        # Add all changes
        success, stdout, stderr = run_git_command("git add .", repo_path)
        if not success:
            print(f"  ❌ Failed to add changes: {stderr}")
            return False
        
        # Commit changes
        commit_message = f"Auto-sync commit for {repo_name} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        success, stdout, stderr = run_git_command(f'git commit -m "{commit_message}"', repo_path)
        if not success:
            print(f"  ❌ Failed to commit changes: {stderr}")
            return False
        
        print(f"  ✅ Changes committed successfully")
    else:
        print(f"  ✨ No changes to commit")
    
    # Check for remote origin
    success, stdout, stderr = run_git_command("git remote -v", repo_path)
    if success and "origin" in stdout:
        print(f"  🌐 Remote origin found")
        
        # Try to pull latest changes
        print(f"  ⬇️  Pulling latest changes...")
        success, stdout, stderr = run_git_command("git pull origin main", repo_path)
        if not success:
            # Try master branch if main fails
            success, stdout, stderr = run_git_command("git pull origin master", repo_path)
        
        if success:
            print(f"  ✅ Successfully pulled latest changes")
        else:
            print(f"  ⚠️  Pull may have failed: {stderr}")
        
        # Try to push changes
        print(f"  ⬆️  Pushing changes...")
        success, stdout, stderr = run_git_command("git push origin main", repo_path)
        if not success:
            # Try master branch if main fails
            success, stdout, stderr = run_git_command("git push origin master", repo_path)
        
        if success:
            print(f"  ✅ Successfully pushed changes")
        else:
            print(f"  ⚠️  Push may have failed: {stderr}")
    else:
        print(f"  📍 No remote origin configured")
        print(f"  💡 To add remote: git remote add origin <repository-url>")
    
    return True

def main():
    """Main synchronization function"""
    print("=" * 70)
    print("BRIDGEGAD REPOSITORIES SYNCHRONIZATION")
    print("=" * 70)
    
    # Get all BridgeGAD applications
    base_path = Path("C:/Users/Rajkumar")
    apps = []
    for i in range(13):
        app_path = base_path / f"BridgeGAD-{i:02d}"
        if app_path.exists():
            apps.append(app_path)
    
    print(f"Found {len(apps)} BridgeGAD applications to synchronize")
    
    results = {}
    
    # Synchronize each repository
    for app_path in apps:
        try:
            results[app_path.name] = sync_repository(app_path)
        except Exception as e:
            print(f"  ❌ Error synchronizing {app_path.name}: {e}")
            results[app_path.name] = False
    
    # Generate summary
    print("\\n" + "=" * 70)
    print("SYNCHRONIZATION SUMMARY")
    print("=" * 70)
    
    successful = sum(results.values())
    total = len(results)
    
    for app_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{app_name:15} {status}")
    
    print(f"\\nOverall: {successful}/{total} repositories synchronized")
    
    # Save synchronization log
    output_dir = Path("C:/Users/Rajkumar/BridgeGAD-03/OUTPUT_01_16092025")
    log_file = output_dir / "repository_sync_log.txt"
    
    with open(log_file, 'w') as f:
        f.write("BridgeGAD Repository Synchronization Log\\n")
        f.write("=" * 50 + "\\n")
        f.write(f"Sync Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
        f.write(f"Total Repositories: {total}\\n")
        f.write(f"Successfully Synchronized: {successful}\\n")
        f.write(f"Failed: {total - successful}\\n\\n")
        f.write("Individual Results:\\n")
        for app_name, success in results.items():
            status = "SUCCESS" if success else "FAILED"
            f.write(f"  {app_name}: {status}\\n")
    
    print(f"\\n📋 Synchronization log saved to: {log_file}")
    
    if successful == total:
        print("\\n🎉 All repositories synchronized successfully!")
    else:
        print(f"\\n⚠️  {total - successful} repositories need manual attention")

if __name__ == "__main__":
    main()
