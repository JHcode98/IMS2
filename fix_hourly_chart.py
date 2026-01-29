import os
import sys
from datetime import datetime

class LayoutFixer:
    def __init__(self, html_file='daily_cycle_count.html'):
        self.html_file = html_file
        self.content = None
        self.success = False
        
    def load_file(self):
        """Load the HTML file"""
        try:
            if not os.path.exists(self.html_file):
                print(f"❌ File not found: {self.html_file}")
                return False
            
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.content = f.read()
            print(f"✅ Loaded {self.html_file} ({len(self.content)} characters)")
            return True
        except Exception as e:
            print(f"❌ Error loading file: {str(e)}")
            return False
    
    def backup_file(self):
        """Create a backup"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self.html_file}.backup_{timestamp}"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(self.content)
            print(f"✅ Backup created: {backup_file}")
            return True
        except Exception as e:
            print(f"⚠️  Backup failed: {str(e)}")
            return False
    
    def apply_layout_fix(self):
        """Apply the layout fixes"""
        print("\n📝 Applying Layout Fixes...")
        
        # Old right column section
        old_right_column = '''            <!-- Right Column: Hourly Output Chart + Analytics -->
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

                <!-- Embedded Hourly View (Hidden by default) -->
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
                <div style="display: flex; flex-direction: column; flex: 1;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <h4 style="margin:0;">Analytics Overview</h4>
                        <input type="date" id="ts-analytics-date-filter" style="padding:2px 5px; border:1px solid #ccc; border-radius:4px; font-size:12px; color:#333;" title="Filter Analytics Date">
                    </div>
                    <div id="ts-analytics-content" style="overflow-y: auto;"></div>
                </div>
            </div>'''
        
        # New improved right column section
        new_right_column = '''            <!-- Right Column: Hourly Output Chart + Analytics -->
            <div style="width: 40%; display:flex; flex-direction:column; border-left:1px solid #eee; padding-left:20px; gap: 15px; overflow-y: auto; min-width: 350px;">
                
                <!-- Hourly Output Chart Section -->
                <div class="card" style="margin:0; padding:12px; display:flex; flex-direction:column; border:1px solid #eee; box-shadow:none; flex-shrink: 0; max-height: 400px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <h4 style="margin:0; font-size:14px;" id="ts-hourly-chart-title">Hourly Output (Today)</h4>
                        <button id="ts-view-hourly-full-btn" class="icon-btn" title="View Full Report" style="background:#2752a7; color:white; font-size:11px; padding:4px 8px; border-radius:4px; cursor:pointer;">Full Report</button>
                    </div>
                    <div style="flex:1; position:relative; width:100%; min-height:250px; border:1px solid #eee; border-radius:4px; padding:8px; background:#fff; overflow: hidden;">
                        <canvas id="ts-hourly-chart" style="max-width:100%;"></canvas>
                    </div>
                </div>

                <!-- Embedded Hourly View (Hidden by default) -->
                <div id="embedded-hourly-view" class="card" style="margin:0; padding:10px; display:none; flex-direction:column; border:1px solid #eee; box-shadow:none; flex-shrink: 0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <div style="display:flex; align-items:center; gap:5px;">
                            <button id="toggle-embedded-hourly-btn" class="icon-btn" title="Collapse" style="padding:2px; height:24px; width:24px; border:none; background:none; cursor:pointer;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;"><polyline points="6 9 12 15 18 9"></polyline></svg></button>
                            <h4 style="margin:0; font-size:13px;" id="embedded-hourly-title">Hourly Output Details</h4>
                        </div>
                        <button id="embedded-save-btn" class="icon-btn" style="background:#2752a7; color:white; font-size:11px; padding:4px 8px; border-radius:4px; cursor:pointer;">Save Data</button>
                    </div>
                    <div id="embedded-hourly-content">
                        <div style="height:200px; position:relative; width:100%; flex-shrink: 0; border:1px solid #eee; border-radius:4px; overflow:hidden;">
                            <canvas id="embedded-hourly-chart" style="max-width:100%;"></canvas>
                        </div>
                        <div id="embedded-hourly-details" style="margin-top:10px; overflow-x:auto; max-height:200px; border:1px solid #eee; border-radius:4px;"></div>
                    </div>
                </div>

                <!-- Analytics Overview -->
                <div style="display:flex; flex-direction:column; flex:1; min-height:200px; padding:12px; background:#f8f9fa; border:1px solid #eee; border-radius:6px; overflow:hidden;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-shrink:0;">
                        <h4 style="margin:0; font-size:14px; color:#2752a7;">Analytics Overview</h4>
                        <input type="date" id="ts-analytics-date-filter" style="padding:4px 6px; border:1px solid #ccc; border-radius:4px; font-size:11px; color:#333; cursor:pointer;" title="Filter Analytics by Date">
                    </div>
                    <div id="ts-analytics-content" style="overflow-y:auto; flex:1; padding:8px; background:#fff; border:1px solid #eee; border-radius:4px;"></div>
                </div>
            </div>'''
        
        if old_right_column in self.content:
            self.content = self.content.replace(old_right_column, new_right_column)
            print("✅ Layout fixes applied successfully!")
            return True
        else:
            print("❌ Could not find right column section to update")
            print("   The HTML structure may have changed.")
            return False
    
    def save_file(self):
        """Save the modified file"""
        try:
            with open(self.html_file, 'w', encoding='utf-8') as f:
                f.write(self.content)
            print(f"\n✅ File saved: {self.html_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving file: {str(e)}")
            return False
    
    def run(self):
        """Execute all steps"""
        print("="*60)
        print("TIMESTAMP MODAL - LAYOUT FIXES")
        print("="*60 + "\n")
        
        if not self.load_file():
            return False
        
        self.backup_file()
        
        if not self.apply_layout_fix():
            print("\n❌ Layout fix failed!")
            return False
        
        if not self.save_file():
            return False
        
        print("\n" + "="*60)
        print("✅ ALL LAYOUT FIXES APPLIED SUCCESSFULLY!")
        print("="*60)
        print("\n📋 Changes Made:")
        print("   ✓ Improved chart section spacing and sizing")
        print("   ✓ Better analytics container layout")
        print("   ✓ Fixed scrolling behavior")
        print("   ✓ Added responsive min-width")
        print("   ✓ Improved typography and spacing")
        print("   ✓ Enhanced visual hierarchy")
        print("\n🔄 Reload your browser to see the changes!")
        print("="*60 + "\n")
        
        return True

if __name__ == '__main__':
    fixer = LayoutFixer()
    success = fixer.run()
    sys.exit(0 if success else 1)