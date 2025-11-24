# app_ultimate.py
"""
AI Startup Validator with Enhanced Detailed Report Generation
"""

import streamlit as st
import time
from datetime import datetime
import json
from src.main_orchestrator import StartupValidatorOrchestrator
import base64

# Page config
st.set_page_config(
    page_title="AI Startup Validator",
    page_icon="🚀",
    layout="wide"
)

# Professional CSS remains the same
st.markdown("""
<style>
    .report-container {
        background: white;
        padding: 40px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    .report-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
    }
    .report-title {
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .score-display {
        font-size: 72px;
        font-weight: bold;
        color: #667eea;
        text-align: center;
        margin: 30px 0;
    }
    .verdict-badge {
        display: inline-block;
        padding: 15px 30px;
        border-radius: 50px;
        font-size: 24px;
        font-weight: bold;
        color: white;
        margin: 20px 0;
    }
    .verdict-go {
        background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
    }
    .verdict-pivot {
        background: linear-gradient(135deg, #F59E0B 0%, #FCD34D 100%);
    }
    .verdict-nogo {
        background: linear-gradient(135deg, #EF4444 0%, #F87171 100%);
    }
    .section-title {
        color: #1f2937;
        font-size: 24px;
        font-weight: bold;
        margin: 30px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
    }
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin: 20px 0;
    }
    .metric-box {
        background: #f3f4f6;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .metric-label {
        color: #6b7280;
        font-size: 14px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #1f2937;
        font-size: 24px;
        font-weight: bold;
    }
    .recommendation-box {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
        border-left: 4px solid #3B82F6;
    }
    .insight-box {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize
if 'orchestrator' not in st.session_state:
    with st.spinner("Loading AI agents..."):
        st.session_state.orchestrator = StartupValidatorOrchestrator()
        
if 'results' not in st.session_state:
    st.session_state.results = None

# Header
st.title("🚀 AI Startup Validator - Professional Edition")
st.markdown("**Get a comprehensive validation report for your startup idea**")
st.markdown("---")

# Input Section
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Enter Your Startup Idea")
    
    startup_idea = st.text_area(
        "Describe your startup idea in detail:",
        height=150,
        placeholder="Example: An AI-powered mental health platform for university students..."
    )
    
    col_a, col_b = st.columns(2)
    with col_a:
        founder_name = st.text_input("Your Name (for report)", "Founder")
    with col_b:
        company_name = st.text_input("Company Name (optional)", "")
    
    if st.button("🚀 Generate Validation Report", type="primary", use_container_width=True):
        if len(startup_idea) < 20:
            st.error("Please provide more details about your idea")
        else:
            with st.spinner("Generating comprehensive report... (15-30 seconds)"):
                # Animated progress
                progress = st.progress(0)
                for i in range(0, 100, 20):
                    progress.progress(i)
                    time.sleep(0.5)
                
                # Run validation
                results = st.session_state.orchestrator.validate_idea(startup_idea)
                st.session_state.results = results
                st.session_state.founder_name = founder_name
                st.session_state.company_name = company_name or "Your Startup"
                st.session_state.idea = startup_idea
                
                progress.progress(100)
                st.success("✅ Report generated successfully!")

with col2:
    st.info("""
    **What you'll get:**
    - Validation Score (0-10)
    - GO/PIVOT/NO-GO Verdict
    - Market Analysis ($TAM, SAM, SOM)
    - Competitive Landscape
    - Technical Requirements
    - Financial Projections
    - Strategic Recommendations
    - Detailed Action Plan
    - Risk Assessment
    - Downloadable Report
    """)

# Report Section
if st.session_state.results:
    results = st.session_state.results
    summary = results.get('summary', {})
    
    st.markdown("---")
    st.header("📊 Your Comprehensive Validation Report")
    
    # Generate Enhanced HTML Report with MORE details
    def generate_html_report():
        score = summary.get('score', 0)
        verdict = summary.get('verdict', 'Unknown')
        
        # Determine verdict styling
        if 'GO' in verdict:
            verdict_class = 'verdict-go'
            verdict_color = '#10B981'
        elif 'PIVOT' in verdict:
            verdict_class = 'verdict-pivot'
            verdict_color = '#F59E0B'
        else:
            verdict_class = 'verdict-nogo'
            verdict_color = '#EF4444'
        
        # Extract detailed information
        market_insights = results.get('market_analysis', {}).get('market_research', {}).get('market_insights', [])
        market_sources = results.get('market_analysis', {}).get('market_research', {}).get('sources', [])
        competitors = results.get('competitor_analysis', {}).get('competitor_list', [])
        competitor_details = results.get('competitor_analysis', {}).get('detailed_analysis', [])
        market_gaps = results.get('competitor_analysis', {}).get('market_gaps', {})
        growth_data = results.get('market_analysis', {}).get('trends', {})
        growth_rates = growth_data.get('growth_rates_found', [])
        startup_costs = results.get('financial_analysis', {}).get('startup_costs', {})
        revenue_proj = results.get('financial_analysis', {}).get('revenue_projections', {})
        break_even = results.get('financial_analysis', {}).get('break_even_analysis', {})
        tech_stack = results.get('technical_analysis', {}).get('tech_stack', {})
        complexity_data = results.get('technical_analysis', {}).get('complexity', {})
        timeline_data = results.get('technical_analysis', {}).get('timeline', {})
        
        # Data quality indicators
        using_real_data = results.get('using_real_data', False)
        confidence_score = results.get('confidence_score', 75)
        market_data_source = results.get('market_analysis', {}).get('data_source', 'Estimated')
        competitor_data_source = results.get('competitor_analysis', {}).get('data_source', 'Estimated')
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{st.session_state.company_name} - AI Startup Validation Report</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
                    line-height: 1.6;
                    color: #1f2937;
                    background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
                    padding: 20px;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
                    overflow: hidden;
                }}
                
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 60px 40px;
                    text-align: center;
                    position: relative;
                    overflow: hidden;
                }}
                
                .header::before {{
                    content: "";
                    position: absolute;
                    top: -50%;
                    right: -50%;
                    width: 200%;
                    height: 200%;
                    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                    animation: rotate 30s linear infinite;
                }}
                
                @keyframes rotate {{
                    from {{ transform: rotate(0deg); }}
                    to {{ transform: rotate(360deg); }}
                }}
                
                .header h1 {{
                    font-size: 48px;
                    margin-bottom: 10px;
                    font-weight: 700;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                    position: relative;
                    z-index: 1;
                }}
                
                .company-name {{
                    font-size: 30px;
                    opacity: 0.95;
                    margin-bottom: 10px;
                    position: relative;
                    z-index: 1;
                }}
                
                .date {{
                    font-size: 16px;
                    opacity: 0.8;
                    position: relative;
                    z-index: 1;
                }}
                
                .score-section {{
                    background: white;
                    padding: 60px 40px;
                    text-align: center;
                    border-bottom: 1px solid #e5e7eb;
                }}
                
                .score-circle {{
                    display: inline-block;
                    width: 200px;
                    height: 200px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 72px;
                    font-weight: bold;
                    box-shadow: 0 15px 50px rgba(102, 126, 234, 0.4);
                    margin: 30px auto;
                }}
                
                .verdict-badge {{
                    display: inline-block;
                    padding: 20px 60px;
                    border-radius: 50px;
                    font-size: 36px;
                    font-weight: bold;
                    color: white;
                    background: linear-gradient(135deg, {verdict_color} 0%, {verdict_color}dd 100%);
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    margin: 20px 0;
                }}
                
                .confidence-meter {{
                    max-width: 600px;
                    margin: 40px auto;
                    padding: 25px;
                    background: #f9fafb;
                    border-radius: 15px;
                }}
                
                .confidence-bar {{
                    width: 100%;
                    height: 35px;
                    background: #e5e7eb;
                    border-radius: 20px;
                    overflow: hidden;
                    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
                }}
                
                .confidence-fill {{
                    height: 100%;
                    width: {confidence_score}%;
                    background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    transition: width 2s ease-in-out;
                }}
                
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                    gap: 25px;
                    padding: 30px;
                }}
                
                .metric-card {{
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    padding: 25px;
                    border-radius: 15px;
                    border-left: 5px solid #667eea;
                    transition: transform 0.3s, box-shadow 0.3s;
                }}
                
                .metric-card:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }}
                
                .metric-label {{
                    font-size: 13px;
                    text-transform: uppercase;
                    color: #6b7280;
                    letter-spacing: 1.2px;
                    margin-bottom: 10px;
                    font-weight: 600;
                }}
                
                .metric-value {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #1f2937;
                    line-height: 1.2;
                }}
                
                .section {{
                    padding: 50px;
                    border-bottom: 1px solid #e5e7eb;
                }}
                
                .section-title {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #1f2937;
                    margin-bottom: 30px;
                    padding-bottom: 15px;
                    border-bottom: 3px solid #667eea;
                    display: flex;
                    align-items: center;
                    gap: 15px;
                }}
                
                .data-source-badge {{
                    display: inline-block;
                    padding: 6px 18px;
                    background: {'#10b981' if using_real_data else '#f59e0b'};
                    color: white;
                    border-radius: 25px;
                    font-size: 14px;
                    font-weight: normal;
                    margin-left: 15px;
                }}
                
                .insight-card {{
                    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
                    padding: 25px;
                    border-radius: 12px;
                    margin: 20px 0;
                    border-left: 5px solid #3b82f6;
                    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
                }}
                
                .competitor-card {{
                    background: white;
                    border: 1px solid #e5e7eb;
                    padding: 25px;
                    border-radius: 12px;
                    margin: 15px 0;
                    transition: all 0.3s;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                }}
                
                .competitor-card:hover {{
                    transform: translateX(10px);
                    box-shadow: 0 5px 25px rgba(0,0,0,0.1);
                    border-color: #667eea;
                }}
                
                .competitor-card h4 {{
                    color: #1f2937;
                    font-size: 20px;
                    margin-bottom: 10px;
                }}
                
                .confidence-label {{
                    display: inline-block;
                    padding: 4px 12px;
                    background: #f3f4f6;
                    color: #6b7280;
                    border-radius: 15px;
                    font-size: 12px;
                    font-weight: 600;
                    text-transform: uppercase;
                }}
                
                .gap-category {{
                    margin: 30px 0;
                }}
                
                .gap-category h4 {{
                    color: #4b5563;
                    margin-bottom: 15px;
                    font-size: 18px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                
                .gap-item {{
                    display: inline-block;
                    padding: 10px 20px;
                    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                    color: #92400e;
                    border-radius: 25px;
                    margin: 5px;
                    font-size: 15px;
                    font-weight: 500;
                    box-shadow: 0 2px 8px rgba(252, 211, 77, 0.3);
                }}
                
                .tech-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-top: 25px;
                }}
                
                .tech-item {{
                    background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    font-weight: 600;
                    font-size: 16px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                    transition: transform 0.3s;
                }}
                
                .tech-item:hover {{
                    transform: translateY(-3px);
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                
                .financial-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 25px;
                    overflow: hidden;
                    border-radius: 10px;
                    box-shadow: 0 2px 15px rgba(0,0,0,0.08);
                }}
                
                .financial-table th {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 18px;
                    text-align: left;
                    font-weight: 600;
                    font-size: 14px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                
                .financial-table td {{
                    padding: 18px;
                    border-bottom: 1px solid #e5e7eb;
                    background: white;
                    font-size: 16px;
                }}
                
                .financial-table tr:last-child td {{
                    border-bottom: none;
                }}
                
                .financial-table tr:hover td {{
                    background: #f9fafb;
                }}
                
                .source-list {{
                    background: #f9fafb;
                    padding: 25px;
                    border-radius: 12px;
                    margin-top: 25px;
                    border: 1px dashed #d1d5db;
                }}
                
                .source-item {{
                    padding: 10px 0;
                    color: #4b5563;
                    font-size: 14px;
                    word-break: break-all;
                    display: flex;
                    align-items: start;
                    gap: 10px;
                }}
                
                .recommendations-list {{
                    counter-reset: recommendation;
                }}
                
                .recommendation {{
                    position: relative;
                    padding: 25px;
                    padding-left: 70px;
                    margin: 20px 0;
                    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                    border-radius: 12px;
                    border-left: 5px solid #0ea5e9;
                    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.1);
                    counter-increment: recommendation;
                    font-size: 16px;
                    transition: transform 0.3s;
                }}
                
                .recommendation:hover {{
                    transform: translateX(10px);
                }}
                
                .recommendation::before {{
                    content: counter(recommendation);
                    position: absolute;
                    left: 25px;
                    top: 50%;
                    transform: translateY(-50%);
                    width: 35px;
                    height: 35px;
                    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
                    color: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 18px;
                    box-shadow: 0 4px 10px rgba(14, 165, 233, 0.3);
                }}
                
                .action-timeline {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                    gap: 30px;
                    margin-top: 35px;
                }}
                
                .timeline-phase {{
                    background: white;
                    border: 2px solid #e5e7eb;
                    border-radius: 15px;
                    padding: 30px;
                    position: relative;
                    transition: all 0.3s;
                }}
                
                .timeline-phase:hover {{
                    border-color: #667eea;
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.15);
                }}
                
                .timeline-phase h4 {{
                    color: #667eea;
                    margin-bottom: 20px;
                    font-size: 22px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                
                .timeline-phase ul {{
                    list-style: none;
                }}
                
                .timeline-phase li {{
                    padding: 12px 0;
                    padding-left: 30px;
                    position: relative;
                    font-size: 15px;
                    line-height: 1.6;
                }}
                
                .timeline-phase li::before {{
                    content: "→";
                    position: absolute;
                    left: 0;
                    color: #667eea;
                    font-weight: bold;
                    font-size: 20px;
                }}
                
                .risk-card {{
                    background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
                    border-left: 5px solid #ef4444;
                    padding: 25px;
                    border-radius: 12px;
                    margin: 20px 0;
                }}
                
                .footer {{
                    background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
                    color: white;
                    padding: 50px;
                    text-align: center;
                }}
                
                .footer h3 {{
                    font-size: 24px;
                    margin-bottom: 20px;
                    color: #f9fafb;
                }}
                
                .footer p {{
                    margin: 8px 0;
                    opacity: 0.9;
                    font-size: 15px;
                }}
                
                @media print {{
                    body {{ 
                        background: white; 
                        padding: 0;
                    }}
                    .container {{ 
                        box-shadow: none; 
                        border-radius: 0;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <!-- Enhanced Header -->
                <div class="header">
                    <h1>AI Startup Validation Report</h1>
                    <div class="company-name">{st.session_state.company_name}</div>
                    <div class="date">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
                </div>
                
                <!-- Score Section with Confidence -->
                <div class="score-section">
                    <h2 style="margin-bottom: 30px; color: #4b5563; font-size: 28px;">Overall Validation Assessment</h2>
                    <div class="score-circle">{score}/10</div>
                    <div class="{verdict_class}">{verdict}</div>
                    
                    <div class="confidence-meter">
                        <h4 style="margin-bottom: 15px; color: #1f2937;">Data Confidence Level</h4>
                        <div class="confidence-bar">
                            <div class="confidence-fill">{confidence_score}%</div>
                        </div>
                        <p style="margin-top: 15px; color: #6b7280; font-size: 14px;">
                            {'Based on real-time market research via Serper API' if using_real_data else 'Based on analytical models and estimates'}
                        </p>
                    </div>
                </div>
                
                <!-- Enhanced Key Metrics -->
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Market Opportunity (TAM)</div>
                        <div class="metric-value">{summary.get('market_size', 'N/A')}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Competition Level</div>
                        <div class="metric-value">{summary.get('competitors_found', 0)} found</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Technical Complexity</div>
                        <div class="metric-value">{summary.get('technical_complexity', 'N/A')}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Initial Investment</div>
                        <div class="metric-value">{summary.get('initial_investment', 'N/A')}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Break-even Timeline</div>
                        <div class="metric-value">{summary.get('break_even', 'N/A')}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Analysis Time</div>
                        <div class="metric-value">{results.get('execution_time', 0):.1f}s</div>
                    </div>
                </div>
                
                <!-- Executive Summary -->
                <div class="section">
                    <h2 class="section-title">
                        💡 Executive Summary
                    </h2>
                    <p style="font-size: 17px; margin-bottom: 15px;"><strong>Startup Idea:</strong> {st.session_state.idea}</p>
                    <p style="font-size: 17px; margin-bottom: 15px;"><strong>Submitted by:</strong> {st.session_state.founder_name}</p>
                    <p style="font-size: 17px; margin-bottom: 15px;"><strong>Analysis Method:</strong> {'Real-time web research using Serper API with 5 specialized AI agents' if using_real_data else 'Multi-agent analytical modeling with industry baselines'}</p>
                    
                    <div style="margin-top: 30px; padding: 25px; background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border-radius: 12px; border-left: 5px solid #22c55e;">
                        <h4 style="color: #166534; margin-bottom: 10px;">Key Finding</h4>
                        <p style="font-size: 16px; line-height: 1.8; color: #166534;">
                            {results.get('strategy', {}).get('summary', 'Comprehensive analysis completed successfully. The validation system has analyzed market opportunity, competitive landscape, technical feasibility, and financial projections to provide actionable insights.')}
                        </p>
                    </div>
                </div>
                
                <!-- Detailed Market Analysis -->
                <div class="section">
                    <h2 class="section-title">
                        📊 Market Analysis
                        <span class="data-source-badge">{'Real Data' if 'Real' in market_data_source else 'Estimated'}</span>
                    </h2>
                    
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-label">Total Addressable Market (TAM)</div>
                            <div class="metric-value">{results.get('market_analysis', {}).get('market_opportunity', {}).get('TAM', {}).get('formatted', 'N/A')}</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Serviceable Available Market (SAM)</div>
                            <div class="metric-value">{results.get('market_analysis', {}).get('market_opportunity', {}).get('SAM', {}).get('formatted', 'N/A')}</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Serviceable Obtainable Market (SOM)</div>
                            <div class="metric-value">{results.get('market_analysis', {}).get('market_opportunity', {}).get('SOM', {}).get('formatted', 'N/A')}</div>
                        </div>
                    </div>
                    
                    <h3 style="margin-top: 40px; margin-bottom: 20px; color: #1f2937;">Market Growth Analysis</h3>
                    <div style="background: #f9fafb; padding: 25px; border-radius: 12px;">
                        <p style="font-size: 16px; margin-bottom: 10px;"><strong>Average Growth Rate:</strong> <span style="font-size: 24px; color: #667eea;">{growth_data.get('average_growth_rate', 'N/A')}</span></p>
                        <p style="font-size: 16px; margin-bottom: 10px;"><strong>Market Phase:</strong> <span style="font-size: 20px; color: #059669;">{growth_data.get('market_phase', 'N/A')}</span></p>
                        {f'<p style="font-size: 16px;"><strong>Growth Rates Found:</strong> {", ".join(growth_rates)}</p>' if growth_rates else ''}
                    </div>
                    
                    """
                    
        # Add market insights section
        market_insights_section = ""
        if market_insights:
            market_insights_section = '<h3 style="margin-top: 40px; margin-bottom: 20px; color: #1f2937;">Market Insights from Research</h3>'
            for insight in market_insights[:3]:
                source = insight.get("source", "Research Finding")
                text = insight.get("insight", "")
                numbers = insight.get("numbers", [])
                numbers_html = f'<div style="margin-top: 10px;"><strong>Key Numbers:</strong> {", ".join(numbers)}</div>' if numbers else ''
                
                market_insights_section += f'''
                <div class="insight-card">
                    <h4 style="color: #1e40af; margin-bottom: 10px;">Source: {source}</h4>
                    <p style="font-size: 15px; line-height: 1.8;">{text}</p>
                    {numbers_html}
                </div>
                '''
        
        html += market_insights_section + """
                    
                    """
                    
        # Add sources section
        sources_section = ""
        if market_sources:
            sources_section = '''
            <div class="source-list">
                <h4 style="margin-bottom: 15px; color: #374151;">Research Sources</h4>
            '''
            for source in market_sources[:5]:
                sources_section += f'<div class="source-item">• {source}</div>'
            sources_section += '</div>'
        
        html += sources_section + """
                </div>
                
                <!-- Enhanced Competitive Landscape -->
                <div class="section">
                    <h2 class="section-title">
                        🎯 Competitive Landscape
                        <span class="data-source-badge">""" + ('Real Search' if 'Real' in competitor_data_source else 'Analysis') + """</span>
                    </h2>
                    
                    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 25px; border-radius: 12px; margin-bottom: 30px;">
                        <p style="font-size: 18px; color: #78350f;"><strong>Total Competitors Identified:</strong> <span style="font-size: 28px;">""" + str(results.get('competitor_analysis', {}).get('competitors_found', 0)) + """</span></p>
                    </div>
                    
                    <h3 style="margin: 30px 0 20px 0; color: #1f2937;">Key Competitors Analysis</h3>
                    """ + ''.join([f'''
                    <div class="competitor-card">
                        <h4>{comp.get('name', 'Unknown')}</h4>
                        <p style="margin: 10px 0; color: #4b5563; line-height: 1.6;">{comp.get('description', 'No description available')[:200]}</p>
                        <span class="confidence-label">Confidence: {comp.get('confidence', 'unknown')}</span>
                    </div>
                    ''' for comp in competitors[:5]]) + """
                    
                    """
                    
        # Add competitor details section  
        competitor_details_section = ""
        if competitor_details:
            for detail in competitor_details[:3]:
                name = detail.get('name', 'Competitor')
                strengths = detail.get('strengths', [])
                weaknesses = detail.get('weaknesses', [])
                funding = detail.get('funding', 'Unknown')
                user_base = detail.get('user_base', 'Unknown')
                
                strengths_html = ''.join([f"<li>{s}</li>" for s in strengths])
                weaknesses_html = ''.join([f"<li>{w}</li>" for w in weaknesses])
                
                competitor_details_section += f'''
                <div style="background: white; border: 2px solid #e5e7eb; padding: 25px; border-radius: 12px; margin: 20px 0;">
                    <h4 style="color: #1f2937; margin-bottom: 15px;">{name}</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div>
                            <h5 style="color: #059669; margin-bottom: 10px;">Strengths:</h5>
                            <ul style="color: #4b5563;">
                                {strengths_html}
                            </ul>
                        </div>
                        <div>
                            <h5 style="color: #dc2626; margin-bottom: 10px;">Weaknesses:</h5>
                            <ul style="color: #4b5563;">
                                {weaknesses_html}
                            </ul>
                        </div>
                    </div>
                    <p style="margin-top: 15px;"><strong>Funding:</strong> {funding}</p>
                    <p><strong>User Base:</strong> {user_base}</p>
                </div>
                '''
        
        html += competitor_details_section + """
                    
                    <h3 style="margin-top: 40px; margin-bottom: 25px; color: #1f2937;">Market Gaps & Opportunities</h3>
                    
                    <div class="gap-category">
                        <h4>📍 Unserved Market Segments</h4>
                        """ + ''.join([f'<span class="gap-item">{gap}</span>' for gap in market_gaps.get('unserved_segments', [])[:4]]) + """
                    </div>
                    
                    <div class="gap-category">
                        <h4>🔧 Missing Features in Market</h4>
                        """ + ''.join([f'<span class="gap-item">{gap}</span>' for gap in market_gaps.get('missing_features', [])[:4]]) + """
                    </div>
                    
                    <div class="gap-category">
                        <h4>💰 Pricing Opportunities</h4>
                        """ + ''.join([f'<span class="gap-item">{gap}</span>' for gap in market_gaps.get('pricing_opportunities', [])[:3]]) + """
                    </div>
                    
                    <div class="gap-category">
                        <h4>🌍 Geographic Gaps</h4>
                        """ + ''.join([f'<span class="gap-item">{gap}</span>' for gap in market_gaps.get('geographic_gaps', [])[:3]]) + """
                    </div>
                </div>
                
                <!-- Technical Assessment -->
                <div class="section">
                    <h2 class="section-title">⚙️ Technical Assessment</h2>
                    
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-label">Complexity Level</div>
                            <div class="metric-value">""" + str(complexity_data.get('complexity', 'N/A')) + """</div>
                            <p style="margin-top: 10px; color: #6b7280; font-size: 14px;">Score: """ + str(complexity_data.get('score', 'N/A')) + """/10</p>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">MVP Timeline</div>
                            <div class="metric-value">""" + str(timeline_data.get('mvp', 'N/A')) + """</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-label">Team Size Required</div>
                            <div class="metric-value">""" + str(timeline_data.get('team_size', 'N/A')) + """</div>
                        </div>
                    </div>
                    
                    <h3 style="margin-top: 40px; margin-bottom: 20px;">Development Timeline</h3>
                    <div style="background: #f9fafb; padding: 25px; border-radius: 12px;">
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
                            <div>
                                <strong>MVP:</strong> """ + str(timeline_data.get('mvp', 'N/A')) + """
                            </div>
                            <div>
                                <strong>Beta:</strong> """ + str(timeline_data.get('beta', 'N/A')) + """
                            </div>
                            <div>
                                <strong>Full Launch:</strong> """ + str(timeline_data.get('launch', 'N/A')) + """
                            </div>
                        </div>
                    </div>
                    
                    <h3 style="margin-top: 40px; margin-bottom: 20px;">Recommended Technology Stack</h3>
                    <div class="tech-grid">
                        """ + (f'<div class="tech-item">Frontend<br><strong>{tech_stack.get("frontend", "N/A")}</strong></div>' if tech_stack.get('frontend') else '') + """
                        """ + (f'<div class="tech-item">Backend<br><strong>{tech_stack.get("backend", "N/A")}</strong></div>' if tech_stack.get('backend') else '') + """
                        """ + (f'<div class="tech-item">Database<br><strong>{tech_stack.get("database", "N/A")}</strong></div>' if tech_stack.get('database') else '') + """
                        """ + (f'<div class="tech-item">Hosting<br><strong>{tech_stack.get("hosting", "N/A")}</strong></div>' if tech_stack.get('hosting') else '') + """
                        """ + (f'<div class="tech-item">Mobile<br><strong>{tech_stack.get("mobile", "N/A")}</strong></div>' if tech_stack.get('mobile') else '') + """
                        """ + (f'<div class="tech-item">Payments<br><strong>{tech_stack.get("payments", "N/A")}</strong></div>' if tech_stack.get('payments') else '') + """
                        """ + ''.join([f'<div class="tech-item">{tech}</div>' for tech in tech_stack.get('additional', [])]) + """
                    </div>
                </div>
                
                <!-- Enhanced Financial Projections -->
                <div class="section">
                    <h2 class="section-title">💰 Financial Projections</h2>
                    
                    <h3 style="margin-bottom: 20px;">Startup Cost Breakdown</h3>
                    <table class="financial-table">
                        <thead>
                            <tr>
                                <th>Category</th>
                                <th>Amount</th>
                                <th>Percentage</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Development</td>
                                <td style="font-weight: 600;">$""" + f"{startup_costs.get('development', 0):,}" + """</td>
                                <td>""" + str(round(startup_costs.get('development', 0) / max(startup_costs.get('total', 1), 1) * 100, 1)) + """%</td>
                            </tr>
                            <tr>
                                <td>Marketing</td>
                                <td style="font-weight: 600;">$""" + f"{startup_costs.get('marketing', 0):,}" + """</td>
                                <td>""" + str(round(startup_costs.get('marketing', 0) / max(startup_costs.get('total', 1), 1) * 100, 1)) + """%</td>
                            </tr>
                            <tr>
                                <td>Operations</td>
                                <td style="font-weight: 600;">$""" + f"{startup_costs.get('operations', 0):,}" + """</td>
                                <td>""" + str(round(startup_costs.get('operations', 0) / max(startup_costs.get('total', 1), 1) * 100, 1)) + """%</td>
                            </tr>
                            <tr>
                                <td>Legal & Compliance</td>
                                <td style="font-weight: 600;">$""" + f"{startup_costs.get('legal', 0):,}" + """</td>
                                <td>""" + str(round(startup_costs.get('legal', 0) / max(startup_costs.get('total', 1), 1) * 100, 1)) + """%</td>
                            </tr>
                            <tr>
                                <td>Other Expenses</td>
                                <td style="font-weight: 600;">$""" + f"{startup_costs.get('other', 0):,}" + """</td>
                                <td>""" + str(round(startup_costs.get('other', 0) / max(startup_costs.get('total', 1), 1) * 100, 1)) + """%</td>
                            </tr>
                            <tr style="background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);">
                                <td style="font-weight: bold; font-size: 18px;">Total Investment Required</td>
                                <td style="font-weight: bold; font-size: 18px; color: #667eea;">""" + str(startup_costs.get('formatted_total', 'N/A')) + """</td>
                                <td style="font-weight: bold;">100%</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <h3 style="margin-top: 40px; margin-bottom: 20px;">Revenue Projections</h3>
                    <table class="financial-table">
                        <thead>
                            <tr>
                                <th>Timeline</th>
                                <th>Projected Revenue</th>
                                <th>Growth</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Year 1</td>
                                <td style="font-weight: 600; color: #059669;">""" + str(revenue_proj.get('year_1_formatted', 'N/A')) + """</td>
                                <td>-</td>
                            </tr>
                            <tr>
                                <td>Year 2</td>
                                <td style="font-weight: 600; color: #059669;">""" + str(revenue_proj.get('year_2_formatted', 'N/A')) + """</td>
                                <td>↑ 200%</td>
                            </tr>
                            <tr>
                                <td>Year 3</td>
                                <td style="font-weight: 600; color: #059669;">""" + str(revenue_proj.get('year_3_formatted', 'N/A')) + """</td>
                                <td>↑ 233%</td>
                            </tr>
                            <tr>
                                <td>Year 5</td>
                                <td style="font-weight: bold; font-size: 18px; color: #059669;">""" + str(revenue_proj.get('year_5_formatted', 'N/A')) + """</td>
                                <td>↑ 150%</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <div style="margin-top: 30px; padding: 25px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 12px;">
                        <h4 style="color: #78350f; margin-bottom: 15px;">Break-even Analysis</h4>
                        <p style="font-size: 16px;"><strong>Time to Break-even:</strong> <span style="font-size: 24px; color: #92400e;">""" + str(break_even.get('break_even_timeline', 'N/A')) + """</span></p>
                        <p style="font-size: 16px;"><strong>Monthly Burn Rate:</strong> """ + str(break_even.get('monthly_burn', 'N/A')) + """</p>
                    </div>
                </div>
                
                <!-- Strategic Recommendations -->
                <div class="section">
                    <h2 class="section-title">🎯 Strategic Recommendations</h2>
                    
                    <div class="recommendations-list">
                        """ + ''.join([f'<div class="recommendation">{rec}</div>' for rec in results.get('strategy', {}).get('recommendations', [])[:5]]) + """
                    </div>
                    
                    <h3 style="margin-top: 40px; margin-bottom: 20px;">Key Success Factors</h3>
                    <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); padding: 25px; border-radius: 12px;">
                        <ul style="list-style: none; padding: 0;">
                            """ + ''.join([f'<li style="padding: 12px; margin: 8px 0; background: white; border-radius: 8px; display: flex; align-items: center; gap: 10px;"><span style="color: #22c55e; font-size: 20px;">✓</span> <strong>{factor}</strong></li>' for factor in results.get('strategy', {}).get('key_success_factors', [])]) + """
                        </ul>
                    </div>
                </div>
                
                <!-- Implementation Roadmap -->
                <div class="section">
                    <h2 class="section-title">📋 Implementation Roadmap</h2>
                    
                    <div class="action-timeline">
                        <div class="timeline-phase">
                            <h4>🚀 Immediate Actions (Week 1)</h4>
                            <ul>
                                """ + ''.join([f'<li>{action}</li>' for action in results.get('strategy', {}).get('action_plan', {}).get('immediate_actions', [])]) + """
                            </ul>
                        </div>
                        
                        <div class="timeline-phase">
                            <h4>📈 30-Day Goals</h4>
                            <ul>
                                """ + ''.join([f'<li>{goal}</li>' for goal in results.get('strategy', {}).get('action_plan', {}).get('30_day_goals', [])]) + """
                            </ul>
                        </div>
                        
                        <div class="timeline-phase">
                            <h4>🎯 90-Day Milestones</h4>
                            <ul>
                                """ + ''.join([f'<li>{goal}</li>' for goal in results.get('strategy', {}).get('action_plan', {}).get('90_day_goals', [])]) + """
                            </ul>
                        </div>
                    </div>
                </div>
                
                <!-- Risk Assessment -->
                <div class="section">
                    <h2 class="section-title">⚠️ Risk Assessment & Mitigation</h2>
                    
                    <div class="risk-card">
                        <h4 style="color: #dc2626; margin-bottom: 15px;">Primary Risk Factors</h4>
                        <ul style="margin-top: 15px; color: #7f1d1d;">
                            <li style="margin: 10px 0;">Market competition intensity: <strong>""" + str(summary.get('competitors_found', 0)) + """ existing players</strong></li>
                            <li style="margin: 10px 0;">Technical complexity level: <strong>""" + str(summary.get('technical_complexity', 'Unknown')) + """</strong></li>
                            <li style="margin: 10px 0;">Capital requirements: <strong>""" + str(summary.get('initial_investment', 'Unknown')) + """</strong></li>
                            <li style="margin: 10px 0;">Time to market: <strong>""" + str(timeline_data.get('mvp', 'Unknown')) + """</strong></li>
                        </ul>
                    </div>
                    
                    <div style="margin-top: 30px; padding: 25px; background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border-radius: 12px;">
                        <h4 style="color: #1e40af; margin-bottom: 15px;">Risk Mitigation Strategies</h4>
                        <ul style="color: #1e3a8a;">
                            <li style="margin: 10px 0;">Start with MVP to validate market demand before full investment</li>
                            <li style="margin: 10px 0;">Focus on underserved market segments identified in gap analysis</li>
                            <li style="margin: 10px 0;">Build strategic partnerships to reduce development costs</li>
                            <li style="margin: 10px 0;">Implement agile development for faster iteration cycles</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Enhanced Footer -->
                <div class="footer">
                    <h3 style="margin-bottom: 25px;">Report Methodology & Data Sources</h3>
                    <p>This comprehensive report was generated using an advanced AI-powered multi-agent validation system.</p>
                    <p style="margin-top: 15px;">
                        <strong>Analysis performed by:</strong> 5 specialized AI agents (Market Analyst, Competitor Researcher, Technical Architect, Financial Analyst, Strategy Advisor)
                    </p>
                    <p style="margin-top: 15px;">
                        <strong>Data Sources:</strong> {'Real-time web research via Serper API, current market reports, and competitor analysis' if using_real_data else 'Industry baselines, analytical models, and historical patterns'}
                    </p>
                    <p style="margin-top: 15px;">
                        <strong>Confidence Score:</strong> {confidence_score}% | <strong>Processing Time:</strong> {results.get('execution_time', 0):.1f} seconds
                    </p>
                    <p style="margin-top: 30px; font-size: 13px; opacity: 0.7;">
                        © 2024 AI Startup Validator - Academic Project<br>
                        Powered by CrewAI Framework, Groq LLM (Llama 3.3), {'Serper API for Real-Time Research' if using_real_data else 'Advanced Analytical Models'}
                    </p>
                    <p style="margin-top: 15px; font-size: 12px; opacity: 0.6;">
                        Disclaimer: This report is generated by AI and should be used as a starting point for decision-making. 
                        Always conduct additional due diligence and consult with industry experts before making investment decisions.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    # Display report preview
    html_report = generate_html_report()
    
    # Show key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Validation Score", f"{summary.get('score', 'N/A')}/10")
    with col2:
        verdict = summary.get('verdict', 'Unknown')
        st.metric("Verdict", verdict)
    with col3:
        st.metric("Market Size", summary.get('market_size', 'N/A'))
    with col4:
        st.metric("Investment", summary.get('initial_investment', 'N/A'))
    
    # Download buttons
    st.markdown("### 📥 Download Your Report")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # HTML download
        b64 = base64.b64encode(html_report.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="startup_validation_report.html">📄 Download HTML Report</a>'
        st.markdown(href, unsafe_allow_html=True)
    
    with col2:
        # JSON download
        json_data = json.dumps(results, indent=2)
        st.download_button(
            label="📊 Download JSON Data",
            data=json_data,
            file_name=f"validation_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col3:
        if st.button("🔄 Validate Another Idea"):
            st.session_state.results = None
            st.rerun()
    
    # Display full report in expandable section
    with st.expander("📋 View Full Report", expanded=True):
        st.components.v1.html(html_report, height=2000, scrolling=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>AI Startup Validator - Professional Validation Reports</p>
    <p>Powered by CrewAI Multi-Agent System | 5 AI Agents | Real-Time Research</p>
</div>
""", unsafe_allow_html=True)