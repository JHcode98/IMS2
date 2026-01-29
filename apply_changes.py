import os
import re
import sys
from datetime import datetime

class ScriptRunner:
    def __init__(self, html_file='daily_cycle_count.html'):
        self.html_file = html_file
        self.content = None
        self.changes_made = []
        self.errors = []
        
    def load_file(self):
        """Load the HTML file with error handling"""
        try:
            if not os.path.exists(self.html_file):
                self.errors.append(f"❌ File not found: {self.html_file}")
                return False
            
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.content = f.read()
            print(f"✅ Loaded {self.html_file} ({len(self.content)} characters)")
            return True
        except Exception as e:
            self.errors.append(f"❌ Error loading file: {str(e)}")
            return False
    
    def backup_file(self):
        """Create a backup of the original file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self.html_file}.backup_{timestamp}"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(self.content)
            print(f"✅ Backup created: {backup_file}")
            return True
        except Exception as e:
            self.errors.append(f"⚠️  Backup failed: {str(e)}")
            return False
    
    def change_1_right_column(self):
        """CHANGE 1: Replace Right Column HTML"""
        print("\n📝 Applying Change 1: Right Column HTML...")
        
        old_section = '''            <!-- Right Column: Analytics & Hourly -->
            <div style="width: 40%; display:flex; flex-direction:column; border-left:1px solid #eee; padding-left:20px; gap: 15px; overflow-y: auto;">
                <!-- Embedded Hourly View -->
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
        
        new_section = '''            <!-- Right Column: Hourly Output Chart + Analytics -->
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
        
        if old_section in self.content:
            self.content = self.content.replace(old_section, new_section)
            self.changes_made.append("✅ Change 1: Right Column HTML - APPLIED")
            return True
        else:
            self.errors.append("❌ Change 1: Could not find right column section to replace")
            return False
    
    def change_2_render_call(self):
        """CHANGE 2: Add renderTsHourlyChart call"""
        print("📝 Applying Change 2: Render Function Call...")
        
        old_call = '''            renderTsAnalytics(sessions, analyticsDate, logsToProcess);
            renderBreakLogTable(logsToProcess, attendance);'''
        
        new_call = '''            renderTsAnalytics(sessions, analyticsDate, logsToProcess);
            renderTsHourlyChart(analyticsDate);
            renderBreakLogTable(logsToProcess, attendance);'''
        
        if old_call in self.content:
            self.content = self.content.replace(old_call, new_call)
            self.changes_made.append("✅ Change 2: Render Function Call - APPLIED")
            return True
        else:
            self.errors.append("❌ Change 2: Could not find render call location")
            return False
    
    def change_3_add_function(self):
        """CHANGE 3: Add renderTsHourlyChart function"""
        print("📝 Applying Change 3: New Function...")
        
        new_function = '''
        function renderTsHourlyChart(date) {
            const ctx = document.getElementById('ts-hourly-chart');
            if (!ctx || typeof Chart === 'undefined') return;
            
            const counters = getCountersData();
            const attendance = getAttendanceData();
            const todayCounters = counters.filter(c => c.date === date);
            
            if (todayCounters.length === 0) {
                if(ctx.parentElement) ctx.parentElement.innerHTML = '<div style="text-align:center; padding:20px; color:#999; height:280px; display:flex; align-items:center; justify-content:center;">No data for ' + date + '</div>';
                return;
            }
            
            const hourlyData = {}, hourlyTargets = {};
            
            for (let h = 6; h < 22; h++) {
                const label = `${h}:00 - ${h+1}:00`;
                hourlyData[label] = 0;
                hourlyTargets[label] = 0;
            }
            
            todayCounters.forEach(counter => {
                if (counter.hourlyActuals) {
                    Object.keys(counter.hourlyActuals).forEach(label => {
                        if (hourlyData.hasOwnProperty(label)) {
                            hourlyData[label] += Number(counter.hourlyActuals[label]) || 0;
                        }
                    });
                }
                
                if (counter.hourlyTargets) {
                    Object.keys(counter.hourlyTargets).forEach(label => {
                        if (hourlyTargets.hasOwnProperty(label)) {
                            hourlyTargets[label] += Number(counter.hourlyTargets[label]) || 0;
                        }
                    });
                } else {
                    const shiftAtt = attendance.filter(a => a.date === date && a.shift === counter.shift);
                    const headcount = shiftAtt.length, rate = Number(counter.standardRate) || 0;
                    const activeTarget = rate > 0 ? (headcount * rate) : (Number(counter.targetOutput) || 0);
                    const defaultHourlyTarget = activeTarget > 0 ? Math.round(activeTarget / 8) : 0;
                    
                    if (counter.shift === "1st Shift-(6am-2pm)") {
                        for (let h = 6; h < 14; h++) hourlyTargets[`${h}:00 - ${h+1}:00`] += defaultHourlyTarget;
                    } else if (counter.shift === "2nd Shift-(2pm-10pm)") {
                        for (let h = 14; h < 22; h++) hourlyTargets[`${h}:00 - ${h+1}:00`] += defaultHourlyTarget;
                    }
                }
            });
            
            const labels = Object.keys(hourlyData), values = Object.values(hourlyData);
            const cumulativeData = [], targetValues = Object.values(hourlyTargets);
            let sum = 0;
            for (const val of values) { sum += val; cumulativeData.push(sum); }
            
            if (window.tsHourlyChart) window.tsHourlyChart.destroy();
            window.tsHourlyChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        { label: 'Hourly Output', data: values, backgroundColor: '#36b9cc', borderColor: '#117a8b', borderWidth: 1, order: 2 },
                        { label: 'Cumulative', data: cumulativeData, type: 'line', borderColor: '#e74c3c', backgroundColor: 'transparent', tension: 0.1, yAxisID: 'y', order: 1, borderWidth: 2 },
                        { label: 'Target', data: targetValues, type: 'line', borderColor: '#27ae60', backgroundColor: 'transparent', tension: 0.1, yAxisID: 'y', borderDash: [5, 5], order: 0, borderWidth: 2 }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { display: true, position: 'top', labels: { font: { size: 11 } } } },
                    scales: { y: { beginAtZero: true, title: { display: true, text: 'Count' } } }
                }
            });
        }
'''
        
        insert_marker = '        function renderInactiveUsersTable(sessions, attendanceData, logs) {'
        insert_position = self.content.find(insert_marker)
        
        if insert_position != -1:
            self.content = self.content[:insert_position] + new_function + '\n        ' + self.content[insert_position:]
            self.changes_made.append("✅ Change 3: New Function - APPLIED")
            return True
        else:
            self.errors.append("❌ Change 3: Could not find insertion point for new function")
            return False
    
    def change_4_button_listener(self):
        """CHANGE 4: Add button event listener"""
        print("📝 Applying Change 4: Button Event Listener...")
        
        button_listener = '''
        const tsViewHourlyFullBtn = document.getElementById('ts-view-hourly-full-btn');
        if (tsViewHourlyFullBtn) {
            tsViewHourlyFullBtn.addEventListener('click', () => {
                const date = document.getElementById('ts-analytics-date-filter').value || new Date().toISOString().split('T')[0];
                openHourlyModal(date, "1st Shift-(6am-2pm)");
            });
        }
'''
        
        analytics_marker = "const tsAnalyticsDateFilter = document.getElementById('ts-analytics-date-filter');"
        analytics_position = self.content.find(analytics_marker)
        
        if analytics_position != -1:
            end_of_line = self.content.find('\n', analytics_position)
            self.content = self.content[:end_of_line+1] + button_listener + self.content[end_of_line+1:]
            self.changes_made.append("✅ Change 4: Button Event Listener - APPLIED")
            return True
        else:
            self.errors.append("❌ Change 4: Could not find analytics date filter definition")
            return False
    
    def save_file(self):
        """Save the modified content to file"""
        try:
            with open(self.html_file, 'w', encoding='utf-8') as f:
                f.write(self.content)
            print(f"\n✅ File saved successfully: {self.html_file}")
            return True
        except Exception as e:
            self.errors.append(f"❌ Error saving file: {str(e)}")
            return False
    
    def print_summary(self):
        """Print summary of changes"""
        print("\n" + "="*60)
        print("SUMMARY OF CHANGES")
        print("="*60)
        
        if self.changes_made:
            print("\n✅ SUCCESSFUL CHANGES:")
            for change in self.changes_made:
                print(f"  {change}")
        
        if self.errors:
            print("\n❌ ERRORS/ISSUES:")
            for error in self.errors:
                print(f"  {error}")
        
        print("\n" + "="*60)
        if not self.errors:
            print("✅ ALL CHANGES APPLIED SUCCESSFULLY!")
            print("✅ The file has been updated with Hourly Output chart integration")
        else:
            print("⚠️  Some changes could not be applied. See errors above.")
        print("="*60 + "\n")
    
    def run(self):
        """Execute all changes"""
        print("="*60)
        print("DAILY CYCLE COUNT - HOURLY OUTPUT CHART INTEGRATION")
        print("="*60 + "\n")
        
        if not self.load_file():
            self.print_summary()
            return False
        
        self.backup_file()
        
        all_success = True
        all_success &= self.change_1_right_column()
        all_success &= self.change_2_render_call()
        all_success &= self.change_3_add_function()
        all_success &= self.change_4_button_listener()
        
        if all_success or len(self.changes_made) > 0:
            self.save_file()
        
        self.print_summary()
        return all_success

if __name__ == '__main__':
    runner = ScriptRunner()
    success = runner.run()
    sys.exit(0 if success else 1)