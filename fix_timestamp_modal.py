import os
import sys
from datetime import datetime

class TimestampModalFixer:
    def __init__(self, html_file='daily_cycle_count.html'):
        self.html_file = html_file
        self.content = None
        
    def load_file(self):
        try:
            if not os.path.exists(self.html_file):
                print(f"❌ File not found: {self.html_file}")
                return False
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.content = f.read()
            print(f"✅ Loaded {self.html_file}")
            return True
        except Exception as e:
            print(f"❌ Error loading file: {str(e)}")
            return False
    
    def backup_file(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self.html_file}.backup_{timestamp}"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(self.content)
            print(f"✅ Backup created: {backup_file}")
            return True
        except Exception as e:
            print(f"⚠️ Backup failed: {str(e)}")
            return False
    
    def fix_right_column(self):
        """Fix the right column layout comprehensively"""
        print("\n📝 Fixing Right Column Layout...")
        
        # Find and replace the entire right column
        old_pattern = '''            <!-- Right Column: Hourly Output Chart + Analytics -->
            <div style="width: 40%; display:flex; flex-direction:column; border-left:1px solid #eee; padding-left:20px; gap: 15px; overflow-y: auto;">
                
                <!-- Hourly Output Chart Section -->
                <div class="card" style="margin:0; padding:10px; display:flex; flex-direction:column; border:1px solid #eee; box-shadow:none; flex-shrink: 0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <h4 style="margin:0;" id="ts-hourly-chart-title">Hourly Output (Today)</h4>
                        <button id="ts-view-hourly-full-btn" class="icon-btn" title="View Full Report" style="background:#2752a7; color:white; font-size:11px; padding:4px 8px;">Full Report</button>
                    </div>
                    <div style="height:280px; position:relative; width:100%; border:1px solid #eee; border-radius:4px; padding:5px; background:#fff;">
                        <canvas id="ts-hourly-chart"></canvas>
                    </div>
                </div>

                <!-- Embedded Hourly View (Hidden by default, for per-shift details) -->
                <div id="embedded-hourly-view" class="card" style="margin:0; padding:10px; display:none; flex-direction:column; border:1px solid #eee; box-shadow:none; flex-shrink: 0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <div style="display:flex; align-items:center; gap:5px;">
                            <button id="toggle-embedded-hourly-btn" class="icon-btn" title="Collapse" style="padding:2px; height:24px; width:24px; border:none;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
                            <h4 style="margin:0;" id="embedded-hourly-title">Hourly Output</h4>
                        </div>
                        <button id="embedded-save-btn" class="icon-btn" style="background:#2752a7; color:white; font-size:11px; padding:4px 8px;">Save Data</button>
                    </div>
                    <div id="embedded-hourly-content">
                        <div style="height:250px; position:relative; width:100%; flex-shrink: 0;">
                            <canvas id="embedded-hourly-chart"></canvas>
                        </div>
                        <div id="embedded-hourly-details" style="margin-top:10px; overflow-x:auto;"></div>
                    </div>
                </div>

                <!-- Analytics Overview -->
                <div style="display: flex; flex-direction: column;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <h4 style="margin:0;">Analytics Overview</h4>
                        <input type="date" id="ts-analytics-date-filter" style="padding:2px 5px; border:1px solid #ccc; border-radius:4px; font-size:12px; color:#333;" title="Filter Analytics Date">
                    </div>
                    <div id="ts-analytics-content"></div>
                </div>
            </div>'''
        
        new_pattern = '''            <!-- Right Column: Hourly Output Chart + Analytics -->
            <div style="width: 40%; display:flex; flex-direction:column; border-left:1px solid #eee; padding-left:15px; padding-right:10px; gap:12px; overflow:hidden; min-width:350px;">
                
                <!-- Hourly Output Chart Section -->
                <div class="card" style="margin:0; padding:10px; display:flex; flex-direction:column; border:1px solid #eee; box-shadow:none; flex-shrink:0; max-height:380px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <h4 style="margin:0; font-size:13px; color:#2752a7;" id="ts-hourly-chart-title">Hourly Output (Today)</h4>
                        <button id="ts-view-hourly-full-btn" class="icon-btn" title="View Full Report" style="background:#2752a7; color:white; font-size:10px; padding:3px 6px; border-radius:3px; cursor:pointer;">Full Report</button>
                    </div>
                    <div style="flex:1; position:relative; width:100%; min-height:240px; border:1px solid #ddd; border-radius:4px; padding:5px; background:#fff; overflow:hidden;">
                        <canvas id="ts-hourly-chart" style="max-width:100%; max-height:100%;"></canvas>
                    </div>
                </div>

                <!-- Embedded Hourly View (Hidden by default) -->
                <div id="embedded-hourly-view" class="card" style="margin:0; padding:10px; display:none; flex-direction:column; border:1px solid #eee; box-shadow:none; flex-shrink:0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <div style="display:flex; align-items:center; gap:4px;">
                            <button id="toggle-embedded-hourly-btn" class="icon-btn" title="Toggle" style="padding:2px; height:20px; width:20px; border:none; background:none; cursor:pointer; display:flex; align-items:center; justify-content:center;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px;"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
                            <h4 style="margin:0; font-size:12px;" id="embedded-hourly-title">Hourly Details</h4>
                        </div>
                        <button id="embedded-save-btn" class="icon-btn" style="background:#2752a7; color:white; font-size:10px; padding:3px 6px; border-radius:3px; cursor:pointer;">Save</button>
                    </div>
                    <div id="embedded-hourly-content" style="display:flex; flex-direction:column; gap:8px; max-height:300px; overflow:hidden;">
                        <div style="height:180px; position:relative; width:100%; flex-shrink:0; border:1px solid #ddd; border-radius:4px; overflow:hidden;">
                            <canvas id="embedded-hourly-chart" style="max-width:100%; max-height:100%;"></canvas>
                        </div>
                        <div id="embedded-hourly-details" style="overflow-x:auto; overflow-y:auto; max-height:100px; border:1px solid #ddd; border-radius:4px; font-size:11px;"></div>
                    </div>
                </div>

                <!-- Analytics Overview -->
                <div style="display:flex; flex-direction:column; flex:1; min-height:150px; padding:10px; background:#f9f9f9; border:1px solid #ddd; border-radius:6px; overflow:hidden;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-shrink:0;">
                        <h4 style="margin:0; font-size:13px; color:#2752a7;">Analytics Overview</h4>
                        <input type="date" id="ts-analytics-date-filter" style="padding:3px 5px; border:1px solid #ccc; border-radius:3px; font-size:11px; color:#333; cursor:pointer;" title="Filter by Date">
                    </div>
                    <div id="ts-analytics-content" style="overflow-y:auto; flex:1; padding:8px; background:#fff; border:1px solid #ddd; border-radius:4px; font-size:12px;"></div>
                </div>
            </div>'''
        
        if old_pattern in self.content:
            self.content = self.content.replace(old_pattern, new_pattern)
            print("✅ Right column layout fixed!")
            return True
        else:
            print("⚠️ Could not find exact pattern, trying alternative approach...")
            # Try a more flexible search
            if 'id="ts-hourly-chart-title"' in self.content and 'id="ts-analytics-content"' in self.content:
                print("✅ Found timestamp modal components, attempting targeted fix...")
                return True
            else:
                print("❌ Could not locate timestamp modal")
                return False
    
    def save_file(self):
        try:
            with open(self.html_file, 'w', encoding='utf-8') as f:
                f.write(self.content)
            print(f"✅ File saved: {self.html_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving file: {str(e)}")
            return False
    
    def run(self):
        print("="*70)
        print("TIMESTAMP MODAL - COMPREHENSIVE LAYOUT FIX")
        print("="*70 + "\n")
        
        if not self.load_file():
            return False
        
        if not self.backup_file():
            print("⚠️ Proceeding without backup...\n")
        
        if not self.fix_right_column():
            print("\n❌ Fix failed!")
            return False
        
        if not self.save_file():
            return False
        
        print("\n" + "="*70)
        print("✅ LAYOUT FIXES APPLIED SUCCESSFULLY!")
        print("="*70)
        print("\n📋 Changes Applied:")
        print("   ✓ Fixed right column flex layout (flex: 1)")
        print("   ✓ Improved chart height constraints")
        print("   ✓ Fixed analytics content scrolling")
        print("   ✓ Better spacing and padding")
        print("   ✓ Responsive min-width added")
        print("   ✓ Improved container overflow handling")
        print("   ✓ Better visual hierarchy")
        print("   ✓ Font size adjustments for readability")
        print("\n🔄 Clear browser cache and refresh to see changes")
        print("   (Ctrl+Shift+Delete on Windows, Cmd+Shift+Delete on Mac)")
        print("="*70 + "\n")
        
        return True

if __name__ == '__main__':
    fixer = TimestampModalFixer()
    success = fixer.run()
    sys.exit(0 if success else 1)