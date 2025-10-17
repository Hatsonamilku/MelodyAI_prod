// advanced-charts.js - Enhanced Analytics Charts
class AdvancedCharts {
    constructor() {
        this.charts = {};
        this.init();
    }

    init() {
        this.initSentimentChart();
        this.initRelationshipChart();
        this.initActivityChart();
    }

    initSentimentChart() {
        const ctx = document.getElementById('sentimentChart');
        if (!ctx) {
            console.log('Sentiment chart element not found');
            return;
        }

        this.charts.sentiment = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Emotional Sentiment',
                    data: [],
                    borderColor: '#74b9ff',
                    backgroundColor: 'rgba(116, 185, 255, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: '💫 Emotional Sentiment Over Time'
                    }
                },
                scales: {
                    y: {
                        min: -1,
                        max: 1,
                        ticks: {
                            callback: function(value) {
                                if (value === 1) return '😊 Very Positive';
                                if (value === 0) return '😐 Neutral';
                                if (value === -1) return '😞 Very Negative';
                                return '';
                            }
                        }
                    }
                }
            }
        });
        console.log('Sentiment chart initialized');
    }

    initRelationshipChart() {
        const ctx = document.getElementById('relationshipChart');
        if (!ctx) {
            console.log('Relationship chart element not found');
            return;
        }

        this.charts.relationship = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Bond Strength', 'Interaction Frequency', 'Emotional Depth', 'Trust Level', 'Engagement'],
                datasets: [{
                    label: 'Relationship Metrics',
                    data: [65, 59, 90, 81, 56],
                    backgroundColor: 'rgba(155, 89, 182, 0.2)',
                    borderColor: 'rgba(155, 89, 182, 1)',
                    pointBackgroundColor: 'rgba(155, 89, 182, 1)'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    r: {
                        angleLines: {
                            display: true
                        },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }
            }
        });
        console.log('Relationship chart initialized');
    }

    initActivityChart() {
        const ctx = document.getElementById('activityChart');
        if (!ctx) {
            console.log('Activity chart element not found');
            return;
        }

        this.charts.activity = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Web', 'Discord', 'Total'],
                datasets: [{
                    label: 'Message Sources',
                    data: [0, 0, 0],
                    backgroundColor: [
                        'rgba(116, 185, 255, 0.8)',
                        'rgba(255, 118, 117, 0.8)',
                        'rgba(155, 89, 182, 0.8)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: '📊 Message Distribution'
                    }
                }
            }
        });
        console.log('Activity chart initialized');
    }

    updateCharts(analyticsData) {
        console.log('Updating charts with data:', analyticsData);
        this.updateSentimentChart(analyticsData);
        this.updateActivityChart(analyticsData);
        this.updateRelationshipChart(analyticsData);
    }

    updateSentimentChart(analyticsData) {
        if (!this.charts.sentiment) {
            console.log('Sentiment chart not available for update');
            return;
        }

        // Create sample sentiment data
        const now = new Date();
        const labels = [];
        const data = [];

        for (let i = 9; i >= 0; i--) {
            const time = new Date(now.getTime() - (i * 10 * 60 * 1000));
            labels.push(time.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}));
            // Use actual sentiment if available, otherwise simulate
            const sentiment = analyticsData.summary?.avg_sentiment || ((Math.random() * 2) - 1);
            data.push(sentiment);
        }

        this.charts.sentiment.data.labels = labels;
        this.charts.sentiment.data.datasets[0].data = data;
        this.charts.sentiment.update();
        console.log('Sentiment chart updated');
    }

    updateActivityChart(analyticsData) {
        if (!this.charts.activity) {
            console.log('Activity chart not available for update');
            return;
        }

        const stats = analyticsData.message_stats || {};
        const webMessages = stats.web_messages || 0;
        const discordMessages = stats.discord_messages || 0;
        
        this.charts.activity.data.datasets[0].data = [
            webMessages,
            discordMessages,
            webMessages + discordMessages
        ];
        this.charts.activity.update();
        console.log('Activity chart updated:', [webMessages, discordMessages]);
    }

    updateRelationshipChart(analyticsData) {
        if (!this.charts.relationship) {
            console.log('Relationship chart not available for update');
            return;
        }

        const relationships = analyticsData.relationship_analytics || {};
        const topRelationship = relationships.top_relationships?.[0];
        
        if (topRelationship) {
            const [user, score] = topRelationship;
            this.charts.relationship.data.datasets[0].data = [
                score, // Bond Strength
                Math.min(100, score + 10), // Interaction Frequency
                Math.min(100, score - 5), // Emotional Depth
                Math.min(100, score + 15), // Trust Level
                Math.min(100, score + 5) // Engagement
            ];
            this.charts.relationship.update();
            console.log('Relationship chart updated for user:', user);
        } else {
            // Default data if no relationships
            this.charts.relationship.data.datasets[0].data = [50, 60, 40, 70, 55];
            this.charts.relationship.update();
            console.log('Relationship chart updated with default data');
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing charts...');
    setTimeout(() => {
        window.advancedCharts = new AdvancedCharts();
        console.log('Advanced charts initialized');
    }, 500);
});