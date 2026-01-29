import os
import sys
from datetime import datetime

class HourlyChartFixer:
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
            print(f"❌ Error: {str(e)}")
            return False
    
    def backup_file(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self.html_file}.backup_{timestamp}"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(self.content)
            print(f"✅ Backup: {backup_file}")
            return True
        except Exception as e:
            print(f"⚠️ Backup failed: {str(e)}")
            return False
    
    def add_function_call(self):
        """Add renderTsHourlyChart call after renderTsAnalytics"""
        print("\n📝 Step 1: Adding function call...")
        
        old_call = '''            renderTsAnalytics(sessions, analyticsDate, logsToProcess);
            renderBreakLogTable(logsToProcess, attendance);'''
        
        new_call = '''            renderTsAnalytics(sessions, analyticsDate, logsToProcess);
            renderTsHourlyChart(analyticsDate);
            renderBreakLogTable(logsToProcess, attendance);'''
        
        if old_call in self.content:
            self.content = self.content.replace(old_call, new_call)
            print("✅ Function call added")
            return True
        else:
            print("❌ Could not find renderTsAnalytics location")
            return False
    
    def add_function_definition(self):
        """Add the renderTsHourlyChart function"""
        print("📝 Step 2: Adding function definition...")
        
        new_function = '''
        function renderTsHourlyChart(date) {
            const ctx = document.getElementById('ts-hourly-chart');
            if (!ctx || typeof Chart === 'undefined') return;
            
            const counters = getCountersData();
            const attendance = getAttendanceData();
            const todayCounters = counters.filter(c => c.date === date);
            
            if (todayCounters.length === 0) {
                if(ctx.parentElement) {
                    ctx.parentElement.innerHTML = '<div style="text-align:center; padding:40px; color:#999; font-size:13px;">No data for ' + date + '</div>';
                }
                return;
            }
            
            const hourlyData = {}, hourlyTargets = {};
            
            // Initialize hours 6-22
            for (let h = 6; h < 22; h++) {
                const label = `${h}:00 - ${h+1}:00`;
                hourlyData[label] = 0;
                hourlyTargets[label] = 0;
            }
            
            // Aggregate data from all shifts
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
                    const headcount = shiftAtt.length;
                    const rate = Number(counter.standardRate) || 0;
                    const activeTarget = rate > 0 ? (headcount * rate) : (Number(counter.targetOutput) || 0);
                    const defaultHourlyTarget = activeTarget > 0 ? Math.round(activeTarget / 8) : 0;
                    
                    if (counter.shift === "1st Shift-(6am-2pm)") {
                        for (let h = 6; h < 14; h++) {
                            hourlyTargets[`${h}:00 - ${h+1}:00`] += defaultHourlyTarget;
                        }
                    } else if (counter.shift === "2nd Shift-(2pm-10pm)") {
                        for (let h = 14; h < 22; h++) {
                            hourlyTargets[`${h}:00 - ${h+1}:00`] += defaultHourlyTarget;
                        }
                    }
                }
            });
            
            const labels = Object.keys(hourlyData);
            const values = Object.values(hourlyData);
            const targetValues = Object.values(hourlyTargets);
            
            // Calculate cumulative
            const cumulativeData = [];
            let sum = 0;
            for (const val of values) {
                sum += val;
                cumulativeData.push(sum);
            }
            
            if (window.tsHourlyChart) window.tsHourlyChart.destroy();
            
            try {
                window.tsHourlyChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [
                            { 
                                label: 'Hourly Output', 
                                data: values, 
                                backgroundColor: '#36b9cc', 
                                borderColor: '#117a8b',
                                borderWidth: 1,
                                order: 2 
                            },
                            { 
                                label: 'Cumulative', 
                                data: cumulativeData, 
                                type: 'line',
                                borderColor: '#e74c3c', 
                                backgroundColor: 'transparent', 
                                tension: 0.2,
                                borderWidth: 2,
                                order: 1 
                            },
                            { 
                                label: 'Target', 
                                data: targetValues, 
                                type: 'line',
                                borderColor: '#27ae60', 
                                backgroundColor: 'transparent', 
                                tension: 0.2,
                                borderDash: [5, 5],
                                borderWidth: 2,
                                order: 0 
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: true, position: 'top', labels: { font: { size: 10 }, padding: 8 } },
                            tooltip: { enabled: true }
                        },
                        scales: {
                            y: { beginAtZero: true }
                        }
                    }
                });
            } catch(e) {
                console.error('Chart error:', e);
            }
        }
'''
        
        # Find insertion point - before renderInactiveUsersTable
        insert_marker = '        function renderInactiveUsersTable(sessions, attendanceData, logs) {'
        insert_pos = self.content.find(insert_marker)
        
        if insert_pos != -1:
            self.content = self.content[:insert_pos] + new_function + '\n        ' + self.content[insert_pos:]
            print("✅ Function definition added")
            return True
        else:
            print("❌ Could not find insertion point")
            return False
    
    def add_button_listener(self):
        """Add button event listener"""
        print("📝 Step 3: Adding button listener...")
        
        listener = '''
        const tsViewHourlyFullBtn = document.getElementById('ts-view-hourly-full-btn');
        if (tsViewHourlyFullBtn) {
            tsViewHourlyFullBtn.addEventListener('click', () => {
                const date = document.getElementById('ts-analytics-date-filter').value || new Date().toISOString().split('T')[0];
                openHourlyModal(date, "1st Shift-(6am-2pm)");
            });
        }
'''
        
        # Find where tsAnalyticsDateFilter is defined
        marker = "const tsAnalyticsDateFilter = document.getElementById('ts-analytics-date-filter');"
        pos = self.content.find(marker)
        
        if pos != -1:
            end_line = self.content.find('\n', pos)
            self.content = self.content[:end_line+1] + listener + self.content[end_line+1:]
            print("✅ Button listener added")
            return True
        else:
            print("⚠️ Could not add button listener (may already exist)")
            return False
    
    def save_file(self):
        try:
            with open(self.html_file, 'w', encoding='utf-8') as f:
                f.write(self.content)
            print(f"\n✅ File saved")
            return True
        except Exception as e:
            print(f"❌ Error saving: {str(e)}")
            return False
    
    def run(self):
        print("="*70)
        print("HOURLY OUTPUT CHART - COMPLETE FIX")
        print("="*70 + "\n")
        
        if not self.load_file():
            return False
        
        self.backup_file()
        
        success = True
        success &= self.add_function_call()
        success &= self.add_function_definition()
        success &= self.add_button_listener()
        
        if success:
            self.save_file()
            print("\n" + "="*70)
            print("✅ ALL FIXES APPLIED SUCCESSFULLY!")
            print("="*70)
            print("\n📋 Changes:")
            print("   ✓ Added renderTsHourlyChart() function")
            print("   ✓ Integrated function call in renderTimestamps()")
            print("   ✓ Added Full Report button listener")
            print("   ✓ Chart will now display hourly data")
            print("\n🔄 Clear cache & refresh browser")
            print("="*70 + "\n")
            return True
        else:
            print("\n❌ Some fixes failed")
            return False

if __name__ == '__main__':
    fixer = HourlyChartFixer()
    success = fixer.run()
    sys.exit(0 if success else 1)