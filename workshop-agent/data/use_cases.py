"""
Framework knowledge and sample use cases for the Agentic Thinking Workshop.
"""

# Discovery workshop coverage areas - what questions should explore
FRAMEWORK_KNOWLEDGE = {
    "coverage_areas": {
        "process_mapping": {
            "name": "Process Mapping",
            "description": "Understanding current state and reimagined future state",
            "key_questions": [
                "What does the current process look like step-by-step?",
                "Where are the bottlenecks and pain points?",
                "What manual steps could be automated?",
                "How would the process change with an AI agent?",
                "What's the gap between current and future state?"
            ]
        },
        "user_value": {
            "name": "User Value Proposition",
            "description": "Why users will adopt and return to the agent",
            "key_questions": [
                "Who are the primary users?",
                "What problem does this solve for them?",
                "Why would users come back to use it repeatedly?",
                "What's the 'aha moment' for users?",
                "How does this make their job easier?"
            ]
        },
        "capabilities": {
            "name": "Capability Mapping",
            "description": "What the agent must be able to do",
            "key_questions": [
                "What are the must-have capabilities?",
                "What are nice-to-have features?",
                "What capabilities drive the core value?",
                "How do we prevent scope creep?",
                "What's the MVP set of capabilities?"
            ]
        },
        "guardrails": {
            "name": "Guardrails & Safety",
            "description": "Boundaries, constraints, and escalation paths",
            "key_questions": [
                "What should the agent NOT do?",
                "When should it escalate to a human?",
                "What are the compliance requirements?",
                "What could go wrong and how do we prevent it?",
                "What decisions are too sensitive for automation?"
            ]
        },
        "data": {
            "name": "Data Mapping",
            "description": "Data sources, quality, and accessibility",
            "key_questions": [
                "What data sources are needed?",
                "Is the data structured or unstructured?",
                "How accessible is the data?",
                "Are there data quality issues?",
                "What are the data gaps?"
            ]
        },
        "roi_metrics": {
            "name": "ROI & Success Metrics",
            "description": "How to measure success and business value",
            "key_questions": [
                "What does success look like?",
                "What are the baseline metrics today?",
                "What's the target improvement?",
                "How will we measure ROI?",
                "What's the go/no-go criteria?"
            ]
        },
        "adoption": {
            "name": "Adoption Strategy",
            "description": "Getting users to actually use the agent",
            "key_questions": [
                "What are the adoption barriers?",
                "Who are the first users/champions?",
                "How will we handle resistance?",
                "What training is needed?",
                "How do we communicate value to users?"
            ]
        },
        "deployment": {
            "name": "Deployment Planning",
            "description": "Rollout strategy and user groups",
            "key_questions": [
                "Who are the first users?",
                "What's the staged rollout plan?",
                "How do we collect feedback?",
                "What's the support model?",
                "How do we iterate based on feedback?"
            ]
        }
    },
    "roles": {
        "agent_owner": {
            "perspective": "Individual agent success, user adoption, daily operations",
            "cares_about": [
                "User satisfaction and adoption rates",
                "Agent performance and reliability",
                "Feedback collection and iteration",
                "Feature prioritization",
                "Escalation handling"
            ],
            "knows_deeply": [
                "Day-to-day user pain points",
                "Specific workflow details",
                "User personas and needs",
                "Adoption barriers",
                "Feedback patterns"
            ]
        },
        "business_owner": {
            "perspective": "Portfolio-level ROI, strategic alignment, resource allocation",
            "cares_about": [
                "Business case and ROI",
                "Strategic fit with company goals",
                "Resource allocation",
                "Risk management",
                "Scale decisions (expand/fix/kill)"
            ],
            "knows_deeply": [
                "Budget constraints",
                "Strategic priorities",
                "Organizational politics",
                "Competing initiatives",
                "Executive expectations"
            ]
        }
    }
}

# Sample use cases with rich hidden details for practice
SAMPLE_USE_CASES = [
    {
        "id": "customer_support_triage",
        "name": "Customer Support Ticket Triage Agent",
        "brief_description": "An AI agent that automatically categorizes and routes incoming customer support tickets.",
        "hidden_details": {
            "current_process": {
                "steps": [
                    "Tickets come in via email, chat, and phone (transcribed)",
                    "L1 support manually reads each ticket (avg 3 min per ticket)",
                    "They categorize into 12 categories with 45 sub-categories",
                    "Tickets are assigned based on agent expertise and availability",
                    "20% of tickets get misrouted, requiring re-assignment"
                ],
                "pain_points": [
                    "High volume during product launches (10x normal)",
                    "Inconsistent categorization between agents",
                    "Senior agents spend 40% of time on simple tickets",
                    "Customer frustration from multiple transfers"
                ],
                "volume": "2,500 tickets/day, 50 support agents"
            },
            "data_landscape": {
                "sources": [
                    "Zendesk ticket history (3 years, 2.7M tickets)",
                    "Product documentation in Confluence",
                    "CRM data in Salesforce",
                    "Agent performance metrics"
                ],
                "quality_issues": [
                    "Historical categorization is inconsistent",
                    "Some tickets missing customer context",
                    "Documentation is outdated in places"
                ]
            },
            "stakeholder_concerns": {
                "agent_owner": {
                    "worries": "Will agents trust the AI? Will it handle edge cases?",
                    "hopes": "Reduce agent burnout, faster resolution times"
                },
                "business_owner": {
                    "worries": "What if we route VIP customers wrong?",
                    "hopes": "Reduce support costs by 30%, improve CSAT"
                }
            },
            "guardrails_needed": [
                "Never auto-respond to VIP customers",
                "Escalate any ticket mentioning legal/lawsuit",
                "Human review for refund requests over $500",
                "Flag potential PR issues for manager review"
            ],
            "success_metrics": {
                "baseline": {
                    "avg_triage_time": "3 minutes",
                    "misroute_rate": "20%",
                    "first_response_time": "4 hours",
                    "csat_score": "3.8/5"
                },
                "targets": {
                    "avg_triage_time": "30 seconds",
                    "misroute_rate": "5%",
                    "first_response_time": "1 hour",
                    "csat_score": "4.3/5"
                }
            },
            "adoption_challenges": [
                "Some senior agents feel threatened",
                "Union concerns about job displacement",
                "Need to prove AI doesn't make more mistakes"
            ]
        }
    },
    {
        "id": "contract_review",
        "name": "Contract Review Assistant",
        "brief_description": "An AI agent that reviews vendor contracts and highlights key terms, risks, and deviations from standard templates.",
        "hidden_details": {
            "current_process": {
                "steps": [
                    "Procurement sends contract to legal inbox",
                    "Legal assistant does initial review (2-3 hours)",
                    "Senior attorney reviews flagged items (1-2 hours)",
                    "Back-and-forth with vendor on redlines (days to weeks)",
                    "Final approval and signature"
                ],
                "pain_points": [
                    "Legal team is bottleneck - 3 week average turnaround",
                    "Junior reviewers miss non-standard clauses",
                    "Same negotiation points come up repeatedly",
                    "No institutional memory of vendor-specific issues"
                ],
                "volume": "150 contracts/month, 4 attorneys"
            },
            "data_landscape": {
                "sources": [
                    "5,000 historical contracts in DocuSign/SharePoint",
                    "Standard template library (12 templates)",
                    "Negotiation playbook (PDF)",
                    "Vendor risk scores from security team"
                ],
                "quality_issues": [
                    "Historical contracts in various formats (PDF, Word, scans)",
                    "Some contracts missing metadata",
                    "Playbook hasn't been updated in 2 years"
                ]
            },
            "stakeholder_concerns": {
                "agent_owner": {
                    "worries": "Legal team resistant to 'AI doing their job'",
                    "hopes": "Free up attorneys for strategic work"
                },
                "business_owner": {
                    "worries": "What if AI misses critical liability clause?",
                    "hopes": "Reduce contract cycle time by 50%"
                }
            },
            "guardrails_needed": [
                "Always require human approval before any response to vendor",
                "Flag contracts over $1M for senior review",
                "Never modify contract text directly",
                "Escalate any IP or indemnification deviations",
                "Cannot access confidential M&A contracts"
            ],
            "success_metrics": {
                "baseline": {
                    "avg_review_time": "5 hours",
                    "turnaround_days": "15 days",
                    "missed_issues_rate": "12%",
                    "attorney_utilization": "80% on routine"
                },
                "targets": {
                    "avg_review_time": "1 hour",
                    "turnaround_days": "5 days",
                    "missed_issues_rate": "3%",
                    "attorney_utilization": "30% on routine"
                }
            },
            "adoption_challenges": [
                "Legal team pride/expertise concerns",
                "Regulatory requirements for human oversight",
                "Building trust in AI recommendations"
            ]
        }
    },
    {
        "id": "sales_proposal",
        "name": "Sales Proposal Generator",
        "brief_description": "An AI agent that helps sales reps create customized proposals by pulling relevant case studies, pricing, and product info.",
        "hidden_details": {
            "current_process": {
                "steps": [
                    "Rep identifies opportunity in Salesforce",
                    "Searches for relevant case studies (30 min avg)",
                    "Pulls pricing from spreadsheet (often outdated)",
                    "Copies from previous proposals (inconsistent)",
                    "Gets manager approval for discounts",
                    "Sends to customer"
                ],
                "pain_points": [
                    "Reps spend 6 hours/week on proposals",
                    "Inconsistent messaging and branding",
                    "Can't find the right case studies",
                    "Pricing errors cause deal delays"
                ],
                "volume": "200 proposals/month, 35 sales reps"
            },
            "data_landscape": {
                "sources": [
                    "Salesforce CRM (opportunities, accounts)",
                    "Case study library in Seismic (500+ studies)",
                    "Pricing engine API",
                    "Product catalog in PIM system",
                    "Competitor battlecards"
                ],
                "quality_issues": [
                    "Case studies tagged inconsistently",
                    "Some pricing rules are tribal knowledge",
                    "Product descriptions vary by region"
                ]
            },
            "stakeholder_concerns": {
                "agent_owner": {
                    "worries": "Will proposals feel generic/robotic?",
                    "hopes": "Reps can focus on relationships, not paperwork"
                },
                "business_owner": {
                    "worries": "Will AI give away too much discount?",
                    "hopes": "Increase proposal volume, improve win rates"
                }
            },
            "guardrails_needed": [
                "Discounts over 20% require manager approval",
                "Cannot include competitor disparagement",
                "Must use approved legal terms only",
                "Cannot promise features not in roadmap",
                "Pricing must validate against current price book"
            ],
            "success_metrics": {
                "baseline": {
                    "time_per_proposal": "3 hours",
                    "proposals_per_rep_week": "4",
                    "pricing_error_rate": "8%",
                    "win_rate": "22%"
                },
                "targets": {
                    "time_per_proposal": "45 minutes",
                    "proposals_per_rep_week": "8",
                    "pricing_error_rate": "1%",
                    "win_rate": "28%"
                }
            },
            "adoption_challenges": [
                "Top reps think their way is better",
                "Fear of losing personal touch",
                "Regional variations in sales process"
            ]
        }
    },
    {
        "id": "employee_onboarding",
        "name": "Employee Onboarding Assistant",
        "brief_description": "An AI agent that guides new hires through their first 90 days, answering questions and coordinating tasks.",
        "hidden_details": {
            "current_process": {
                "steps": [
                    "HR sends welcome email with 20+ links",
                    "Manager creates onboarding checklist (often forgotten)",
                    "New hire figures things out by asking around",
                    "IT provisions access (often delayed)",
                    "Buddy assigned but meetings irregular"
                ],
                "pain_points": [
                    "New hires feel lost, ask same questions",
                    "Managers spend 10+ hours per new hire",
                    "Access/equipment delays waste first week",
                    "30% don't complete compliance training on time"
                ],
                "volume": "50 new hires/month across 8 departments"
            },
            "data_landscape": {
                "sources": [
                    "Workday HRIS (employee data)",
                    "Confluence knowledge base",
                    "IT ticketing system (ServiceNow)",
                    "Learning management system (LMS)",
                    "Department-specific wikis"
                ],
                "quality_issues": [
                    "Knowledge base articles often outdated",
                    "Different departments have different processes",
                    "Some info only exists in people's heads"
                ]
            },
            "stakeholder_concerns": {
                "agent_owner": {
                    "worries": "Will it feel impersonal for new hires?",
                    "hopes": "Consistent experience, faster productivity"
                },
                "business_owner": {
                    "worries": "Sensitive HR questions need human touch",
                    "hopes": "Reduce time-to-productivity by 30%"
                }
            },
            "guardrails_needed": [
                "Escalate benefits/compensation questions to HR",
                "Cannot access performance review data",
                "Flag harassment or discrimination concerns immediately",
                "Cannot modify system access directly",
                "Must verify identity before sharing personal info"
            ],
            "success_metrics": {
                "baseline": {
                    "time_to_productivity": "90 days",
                    "manager_hours_per_hire": "12 hours",
                    "training_completion_rate": "70%",
                    "new_hire_satisfaction": "3.5/5"
                },
                "targets": {
                    "time_to_productivity": "60 days",
                    "manager_hours_per_hire": "4 hours",
                    "training_completion_rate": "95%",
                    "new_hire_satisfaction": "4.5/5"
                }
            },
            "adoption_challenges": [
                "Managers want to keep their own style",
                "Department-specific needs vary widely",
                "Some prefer human interaction"
            ]
        }
    },
    {
        "id": "incident_response",
        "name": "IT Incident Response Coordinator",
        "brief_description": "An AI agent that helps coordinate major IT incidents by gathering context, notifying stakeholders, and tracking resolution.",
        "hidden_details": {
            "current_process": {
                "steps": [
                    "Alert fires from monitoring (PagerDuty)",
                    "On-call engineer investigates manually",
                    "War room created, people pulled in ad-hoc",
                    "Status updates via Slack (inconsistent)",
                    "Post-mortem written (sometimes)"
                ],
                "pain_points": [
                    "Too many alerts, hard to prioritize",
                    "Right people not always engaged quickly",
                    "Stakeholders demand constant updates",
                    "Tribal knowledge about system dependencies",
                    "Post-mortems rarely lead to improvements"
                ],
                "volume": "15 major incidents/month, 200 alerts/day"
            },
            "data_landscape": {
                "sources": [
                    "PagerDuty alerts and schedules",
                    "DataDog metrics and logs",
                    "CMDB (configuration management database)",
                    "Runbooks in Confluence",
                    "Historical incident tickets (Jira)"
                ],
                "quality_issues": [
                    "CMDB is 60% accurate",
                    "Runbooks outdated for newer services",
                    "Alert thresholds not well-tuned"
                ]
            },
            "stakeholder_concerns": {
                "agent_owner": {
                    "worries": "Will engineers trust AI in crisis?",
                    "hopes": "Faster resolution, less toil"
                },
                "business_owner": {
                    "worries": "What if AI makes wrong call during outage?",
                    "hopes": "Reduce MTTR, improve uptime SLAs"
                }
            },
            "guardrails_needed": [
                "Cannot execute remediation commands",
                "Human approval for any customer communication",
                "Escalate security incidents to SecOps immediately",
                "Cannot access production credentials",
                "Must log all recommendations for audit"
            ],
            "success_metrics": {
                "baseline": {
                    "mttr": "45 minutes",
                    "time_to_engage_team": "12 minutes",
                    "stakeholder_update_frequency": "every 30 min",
                    "post_mortem_completion": "60%"
                },
                "targets": {
                    "mttr": "20 minutes",
                    "time_to_engage_team": "3 minutes",
                    "stakeholder_update_frequency": "every 10 min",
                    "post_mortem_completion": "95%"
                }
            },
            "adoption_challenges": [
                "Engineers skeptical of AI in high-stress situations",
                "Existing tools deeply embedded in workflow",
                "Concerns about alert fatigue getting worse"
            ]
        }
    }
]
