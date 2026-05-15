document.addEventListener('DOMContentLoaded', () => {
    
    // --- Mobile Menu Toggle ---
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const closeMenuBtn = document.getElementById('closeMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    if (mobileMenuBtn && mobileMenu && closeMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.remove('hidden');
            mobileMenu.classList.add('flex');
            document.body.style.overflow = 'hidden';
        });

        closeMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.add('hidden');
            mobileMenu.classList.remove('flex');
            document.body.style.overflow = 'auto';
        });
    }

    // --- Animated Counters ---
    const counters = document.querySelectorAll('.counter');
    const speed = 200; // The lower the slower

    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            // Remove commas if any exist currently to parse correctly
            const count = +counter.innerText.replace(/,/g, '');
            const inc = target / speed;

            if (count < target) {
                counter.innerText = (count + inc).toFixed(counter.id === 'retention-rate' ? 1 : 2);
                setTimeout(updateCount, 1);
            } else {
                counter.innerText = target.toLocaleString('en-IN', {
                    minimumFractionDigits: counter.id === 'retention-rate' ? 1 : 2,
                    maximumFractionDigits: counter.id === 'retention-rate' ? 1 : 2
                });
            }
        };
        updateCount();
    });

    // --- Dashboard Specific Logic ---
    const chartDataElement = document.getElementById('chart-data');
    if (chartDataElement) {
        const chartData = JSON.parse(chartDataElement.textContent);
        
        // 1. Health Score Ring Calculation
        const healthScoreVal = document.getElementById('health-score-val');
        const healthRing = document.getElementById('health-ring');
        const healthStatus = document.getElementById('health-status');
        
        let score = 50; // Default baseline
        if (chartData.totalIncome > 0) {
            const ratio = chartData.totalExpense / chartData.totalIncome;
            if (ratio < 0.5) score = 95;
            else if (ratio < 0.8) score = 75;
            else if (ratio < 1.0) score = 50;
            else score = 25;
        } else if (chartData.totalExpense > 0) {
            score = 10; // Expenses but no income = bad
        }
        
        // Animate Score Counter
        let currentScore = 0;
        const scoreInterval = setInterval(() => {
            if (currentScore >= score) {
                clearInterval(scoreInterval);
                healthScoreVal.innerText = score;
            } else {
                currentScore++;
                healthScoreVal.innerText = currentScore;
            }
        }, 20);

        // Update Ring SVG Stroke Dasharray (100 is full circumference)
        setTimeout(() => {
            healthRing.style.strokeDasharray = `${score}, 100`;
            // Change color based on score
            if (score >= 75) {
                healthRing.style.stroke = '#22C55E';
                healthStatus.innerText = 'Optimal';
                healthStatus.style.color = '#22C55E';
            } else if (score >= 50) {
                healthRing.style.stroke = '#F59E0B';
                healthStatus.innerText = 'Warning';
                healthStatus.style.color = '#F59E0B';
            } else {
                healthRing.style.stroke = '#EF4444';
                healthStatus.innerText = 'Critical';
                healthStatus.style.color = '#EF4444';
            }
        }, 500);

        // 2. Smart Budget Galaxy View (Orbs)
        const galaxyContainer = document.getElementById('galaxy-container');
        if (chartData.labels.length > 0) {
            galaxyContainer.innerHTML = ''; // Clear fallback text
            
            const totalExp = chartData.totalExpense || 1;
            
            // Map colors to categories
            const colors = {
                'Food': 'from-orange-500 to-amber-500',
                'Transport': 'from-blue-500 to-cyan-500',
                'Rent': 'from-purple-500 to-indigo-500',
                'Shopping': 'from-pink-500 to-rose-500',
                'Entertainment': 'from-fuchsia-500 to-purple-500',
                'Bills': 'from-emerald-500 to-teal-500',
                'Healthcare': 'from-red-500 to-orange-500',
                'Others': 'from-gray-500 to-slate-500'
            };

            // Calculate positions using a spiral/circular distribution
            const centerX = 50; // percentage
            const centerY = 50; // percentage
            const radius = 35; // max radius percentage
            
            chartData.labels.forEach((label, index) => {
                const amount = chartData.data[index];
                const percentage = (amount / totalExp) * 100;
                
                // Size mapped to percentage (min 60px, max 140px)
                const size = Math.max(60, Math.min(140, 40 + (percentage * 2))); 
                
                // Position logic (circular distribution)
                const angle = (index / chartData.labels.length) * Math.PI * 2;
                const r = radius * (0.5 + (percentage/100)*0.5); // spread out larger ones slightly
                const top = centerY + Math.sin(angle) * r;
                const left = centerX + Math.cos(angle) * r;

                const orb = document.createElement('div');
                const colorClass = colors[label] || 'from-gray-500 to-gray-400';
                
                // Add red glow if category > 30% of expenses
                const glowClass = percentage > 30 ? 'shadow-[0_0_20px_rgba(239,68,68,0.6)] border-red-500/50' : `shadow-lg border-white/20`;

                orb.className = `orb absolute flex items-center justify-center bg-gradient-to-tr ${colorClass} ${glowClass} border float-anim`;
                orb.style.width = `${size}px`;
                orb.style.height = `${size}px`;
                orb.style.top = `calc(${top}% - ${size/2}px)`;
                orb.style.left = `calc(${left}% - ${size/2}px)`;
                orb.style.animationDelay = `${index * 0.5}s`; // staggered floating
                
                orb.innerHTML = `
                    <span class="text-white font-bold text-sm drop-shadow-md z-10">${label}</span>
                    <span class="text-white/80 text-xs font-mono z-10">${percentage.toFixed(0)}%</span>
                `;
                
                // Add tooltip on hover
                orb.title = `${label}: ₹${amount.toLocaleString('en-IN')}`;
                
                galaxyContainer.appendChild(orb);
            });
        }

        // 3. Advanced Charts (Chart.js)
        const ctx = document.getElementById('expenseChart');
        if (ctx && chartData.labels.length > 0) {
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        data: chartData.data,
                        backgroundColor: [
                            'rgba(59, 130, 246, 0.8)', // blue
                            'rgba(139, 92, 246, 0.8)', // purple
                            'rgba(34, 197, 94, 0.8)',  // green
                            'rgba(245, 158, 11, 0.8)', // amber
                            'rgba(236, 72, 153, 0.8)', // pink
                            'rgba(14, 165, 233, 0.8)', // cyan
                            'rgba(239, 68, 68, 0.8)'   // red
                        ],
                        borderColor: '#0F172A',
                        borderWidth: 2,
                        hoverOffset: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '75%', // Makes it a thin futuristic ring
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                color: '#94a3b8',
                                font: {
                                    family: "'Inter', sans-serif"
                                },
                                usePointStyle: true,
                                padding: 20
                            }
                        }
                    }
                }
            });
        }
    }
});
