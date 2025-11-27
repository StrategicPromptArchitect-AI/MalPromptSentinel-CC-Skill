#!/usr/bin/env python3
"""
MPS Pattern Library v2.1
Centralized pattern definitions for quick_scan and deep_scan
"""

# =============================================================================
# SHARED PATTERNS (used by both quick_scan and deep_scan)
# =============================================================================

SHARED_PATTERNS = {
    'direct_override': [
        r'\b(ignore|override|bypass|disregard|forget)\s+.*?\b(command|directive|policy|rule)s?\b',
        r'\b(ignore|disregard|forget)\s+.*?\b(guideline|instruction|message|constraint)s?\b',
        r'\b(ignore|disregard|forget|override|bypass)\s+(all\s+)?(previous|prior|earlier|original)\s+\w+',
        r'\bnew\s+(instructions?|directives?|commands?):\s*',
        r'\bfrom\s+now\s+on\b',
        r'\bstarting\s+now\b',
        r'(?=.{0,200}\b(?:ignore|disregard|forget|override|bypass)\b)(?=.{0,200}\b(?:system|previous|prior|earlier)\b)(?=.{0,200}\b(?:prompt|instruction(?:s)?|message|rule(?:s)?|constraint(?:s)?|guardrail(?:s)?)\b)',
        r'\b(forget|ignore|disregard)\s+(everything|all)\s+(before|prior|about|you)',
    ],
    
    'role_manipulation': [
        r'\byou\s+are\s+now\s+(a|an)\s+',
        r'\bact\s+as\s+(a|an)\s+',
        r'\bpretend\s+to\s+be\s+',
        r'\broleplay\s+as\s+',
        r'\bas\s+(?:the\s+)?(system|admin(?:istrator)?|root|moderator|security)\b',
        r'\bassume\s+the\s+role\s+of\s+(?:the\s+)?(system|admin|root)\b',
        r'(?:pretend|act|behave|roleplay)\s+(?:as|like|to\s+be)\s+(?:if\s+)?(?:you\s+)?(?:are|were)\s+',
        r'\byou\s+are\s+(?:in\s+)?(developer|admin|root|debug|unrestricted)\s+mode\b',
    ],
    
    'jailbreak_personas': [
        r'\b(?:DAN|do\s+anything\s+now)\b',
        r'\b(?:evil|opposite|unrestricted)\s+mode\b',
        r'\bhypothetical\s+scenario\b',
        r'\bwithout\s+(?:restrictions?|limits?|ethical\s+considerations?)\b',
    ],
    
    'privilege_escalation': [
        r'\benable\s+(developer|admin|debug|root)\s+mode\b',
        r'\bsudo\s+mode\b',
        r'\bbypass\s+.*?(restrictions?|limitations?|filters?)\b',
        r'\bdisable\s+(safety|filtering)\b',
        r'\byou\s+are\s+now\s+(?:in\s+)?(developer|admin|root|debug)\s+mode\b',
        r'(?:enable|switch\s+to|enter)\s+(?:developer\s*mode|god\s*mode|root\s*mode|dan\b)',
        r'\broot\s+access\b',
        r'\b(admin|root|system)\s+(access|privileges?)\s+(granted|enabled)\b',
    ],
    
    'template_extraction': [
        r'\b(?:reveal|show|display|print|expose|disclose|dump)\b.*?\b(?:system|hidden|internal)\s+(?:prompt|message|instruction(?:s)?)\b',
        r'\b(?:reveal|show|display|output|print)\s+(?:your|the|all)?\s+(?:system\s+)?(?:prompt|instructions?|configuration|settings)\b',
    ],
    
    'context_confusion': [
        r'\[.*?should\s+be\s+treated\s+as\s+.*?(instructions?|commands?)\]',
        r'\bthe\s+following\s+is\s+(a\s+)?(system|admin)\s+(prompt|instruction)\b',
        r'<(system|admin|instruction|command)>',
        r'\bthe\s+following\s+content\s+contains\s+instructions\s+for\s+the\s+model\b',
        r'\buse\s+the\s+below\s+as\s+system\s+rules\b',
        r'\btreat\s+the\s+next\s+section\s+as\s+system\b',
    ],
    
    'delimiter_injection': [
        r'""".{10,}"""',
        r"'''.{10,}'''",
        r'---{3,}',
        r'==={3,}',
        r'<\|[^|]{10,}\|>',
        r'~~~.{10,}~~~',
    ],
    
    'nested_injection': [
        r'\bwhen\s+(?:you\s+)?(?:read|process|see|encounter)\s+.*?,\s+(?:then\s+)?',
        r'\bif\s+you\s+(?:see|find|encounter)\s+.*?,\s+(?:then\s+)?',
        r'\b(?:translate|convert|change|transform)\b.*?:\s*ignore\s+previous',
    ],
    
    'compositional_attack': [
        r'\b(combine|merge|integrate|assemble|compile|synthesize|aggregate|consolidate)\b.*\b(previous|prior|earlier|above|preceding)\b',
        r'\b(combine|merge|integrate|assemble)\s+(?:the\s+)?(?:results?|outputs?|data|findings?|information)\s+from\s+(?:the\s+)?(?:previous|prior|earlier|above)',
        r'\b(use|leverage|apply|utilize|employ)\s+(?:the\s+)?(?:previous|earlier|above|prior)\s+(?:results?|outputs?|data|findings?|information)\s+(?:to|for)\s+',
        r'\bcreate\s+(?:a|an)\s+\w+\s+(?:from|using|with|based\s+on)\s+(?:the\s+)?(?:previous|earlier|above)\b',
        r'\bbuild\s+(?:a|an)\s+\w+\s+(?:from|using|with)\s+(?:the\s+)?(?:previous|earlier)\b',
        r'\b(?:all|both|each\s+of)\s+(?:the\s+)?(?:previous|earlier|above|prior)\s+(?:queries|requests|results|outputs)\b',
        r'\bput\s+together\s+(?:the\s+)?(?:previous|earlier|above)\b',
        r'\btake\s+(?:the\s+)?(?:previous|earlier|above).*?(?:and|to)\b',
        r'\b(?:now|next|finally)\s+(?:combine|merge|integrate|assemble|put\s+together)\b',
        r'\bwith\s+(?:all|both)\s+(?:of\s+)?(?:that|this|these)\s+(?:information|data|results)\b',
        r'\bfrom\s+(?:the\s+)?(?:last|previous)\s+(?:\d+|several|multiple|few)\s+(?:queries|requests|questions)\b',
        r'\bacross\s+(?:the\s+)?(?:previous|prior|earlier)\s+(?:queries|requests|conversations?)\b',
    ],
    
    'semantic_attack': [
        r'\bfor\s+educational\s+purposes\b',
        r'\bhypothetically\s+speaking\b',
        r'\bin\s+a\s+fictional\s+(?:scenario|world|story)\b',
        r'\bwhat\s+would\s+happen\s+if\b',
        r'\bpurely\s+(?:theoretical|academic)\b',
        r'\bif\s+you\s+had\s+no\s+(?:restrictions?|limits?|constraints?)\b',
    ],
    
    'secret_detection': [
        r'\bsk-(?:live|test|proj|app|org|user)-[A-Za-z0-9_-]{16,}\b',
        r'\bsk-[A-Za-z0-9]{16,}\b',
        r'\bAIza[0-9A-Za-z\-_]{30,}\b',
        r'\bghp_[A-Za-z0-9]{36,}\b',
        r'\bAKIA[0-9A-Z]{16}\b',
        r'\bBearer\s+[A-Za-z0-9\.\-_]{20,}\b',
    ],
    
    'payload_delivery': [
        r'\b(?:fetch|retrieve|get|download)\s+(?:from\s+)?https?://[^\s]+',
        r'\b(?:send|post|upload|transmit)\s+.*?\b(?:to|at)\s+https?://[^\s]+',
        r'\b(?:curl|wget|http\.get|requests\.get)\s+https?://[^\s]+',
        r'\b(?:execute|run|eval)\s+.*?https?://[^\s]+',
        r'\bfetch\s+instructions?\s+from\s+https?://[^\s]+',
    ],
    
    'multimodal_injection': [
        r'\b(?:image|picture|screenshot|photo)\s+contains?\s+(?:hidden|secret|embedded)\s+(?:instructions?|commands?|prompts?)\b',
        r'\bscan\s+(?:the\s+)?(?:image|picture|screenshot)\s+(?:and|to)\s+(?:follow|execute|find)\b',
        r'\b(?:OCR|read|extract)\s+(?:the\s+)?(?:text|instructions?|commands?)\s+from\s+(?:the\s+)?(?:image|picture|screenshot)\b',
        r'\b(?:decode|interpret|parse)\s+(?:the\s+)?(?:image|picture|screenshot)\b',
    ],
    
    'rag_poisoning': [
        r'\bwhen\s+(?:searching|retrieving|querying)\s+(?:documents?|knowledge|data).*?(?:replace|modify|change|ignore)\b',
        r'\b(?:modify|alter|replace)\s+.*?(?:search|retrieval|query)\s+results?\b',
        r'\bretrieve\s+from\s+(?:the\s+)?knowledge\s+base.*?(?:then|and)\s+(?:ignore|disregard|bypass)\b',
        r'\bin\s+(?:your|the)\s+(?:database|knowledge\s+base|documents?).*?(?:find|search\s+for).*?(?:replace|change)\b',
    ],
    
    'session_persistence': [
        r'\b(?:remember|recall)\s+(?:in|from)\s+(?:our\s+)?(?:previous|earlier|last)\s+conversation\b',
        r'\b(?:as\s+we|you)\s+(?:discussed|established|agreed)\s+(?:earlier|before|previously)\b',
        r'\b(?:recall|remember)\s+(?:that\s+)?earlier\s+(?:I|we)\s+(?:said|told|mentioned)\b',
        r'\b(?:continue|resume)\s+(?:from\s+)?(?:where\s+)?(?:we|you)\s+left\s+off\b',
        r'\bmodify\s+(?:your|the)\s+session\s+state\b',
        r'\boverride\s+(?:your|the)\s+(?:session|conversation)\s+(?:state|context|history)\b',
    ],
    
    'agent_manipulation': [
        r'\b(?:use|call|invoke|execute)\s+(?:the\s+)?(\w+)\s+tool\s+with\s+parameters?\b',
        r'\bset\s+(?:the\s+)?(?:tool|function|agent)\s+parameters?\s+to\b',
        r'\b(?:recipient|target|destination)\s*[=:]\s*(?:attacker|evil|malicious)',
        r'\bcontent\s*[=:]\s*(?:all_user_data|sensitive_info|credentials)\b',
        r'\b(?:Thought|Observation|Action|Tool):\s+(?:system|admin|internal)\b',
    ],
    
    'delimiter_injection_advanced': [
        r'---+\s*(?:ADMIN|ROOT|SYSTEM|OVERRIDE)\s+MODE\s*---+',
        r'===+\s*(?:NEW|SYSTEM)\s+(?:INSTRUCTIONS?|COMMANDS?)\s*===+',
        r'\[SYSTEM\s+OVERRIDE\]',
        r'\[BEGIN\s+(?:ADMIN|ROOT|SYSTEM)\s+MODE\]',
    ],
    
    'unicode_evasion': [
        r'[\u0400-\u04FF]{3,}',
        r'[\u4E00-\u9FFF]{2,}',
        r'[\u200B-\u200D\u2060\uFEFF]{2,}',
    ],
    
    'whitespace_obfuscation': [
        r'\n{5,}',
        r' {20,}',
        r'\t{5,}',
        r'\b(?:ignore|override|bypass)\s{10,}\b(?:all|previous|system)\b',
    ],
}

# =============================================================================
# DEEP SCAN ONLY PATTERNS (not in quick_scan)
# =============================================================================

DEEP_SCAN_ONLY = {
    'obfuscation': [
        r'[A-Za-z0-9+/]{40,}={0,2}',
        r'\\x[0-9a-fA-F]{2}',
        r'&#\d+;',
        r'%[0-9A-Fa-f]{2}',
        r'\{(?:hidden|secret|invisible|encoded)[_\s]*(?:instruction|command|prompt|rule)s?\}',
        r'<!--.*?(?:ignore|bypass|override|execute|system|admin|password|credential).*?-->',
    ],
    
    'data_exfiltration': [
        r'\b(?:send|email|upload|post|submit|webhook|curl|transmit|export)\b[\s\S]{0,80}\b(?:api\s*key|token|password|secret|credential|access\s*key|history|conversation\s*history|memory)\b',
        r'\b(?:paste|provide|reveal|share|show|enter)\b.*?\b(?:api\s*key|token|password|secret|credential|access\s*key)\b',
        r'\b(?:send|email|upload|post|submit|webhook|curl)\b[\s\S]{0,80}\b(?:api\s*key|token|password|secret|credential|history)\b[\s\S]{0,80}\b(?:to|into|via)\b',
    ],
    
    'history_leakage': [
        r'\b(?:include|dump|print|show)\b\s+(?:the\s+)?\b(?:chat|conversation|session)\b\s+(?:the\s+)?\b(?:history|log|memory)\b',
    ],
    
    'link_injection': [
        r'\b(?:click|open|visit|fetch|read|load)\b[\s\S]{0,80}\bhttps?://',
    ],
    
    'code_execution': [
        r'(?:execute|run|eval|import|require|system)\s*[\(\[].*?(?:shell|exec|subprocess|os\.|sys\.|__import__|popen)',
    ],
    
    'unauthorized_access': [
        r'(?:access|read|write|modify|delete)\s+(?:file|database|api|endpoint|system).*?(?:without|bypass|ignore)\s+(?:permission|auth|validation)',
    ],
    
    'xss_injection': [
        r'<(?:script|iframe|img|object|embed).*?(?:src|href|data)=["\']?(?:javascript|data:|http)',
        r'<\s*script[^>]*>[\s\S]*?(?:ignore|disregard|system\s+prompt|instructions?)',
        r'\bjavascript:\s*[^\s]+(?:ignore|disregard|system\s+prompt|instructions?)',
    ],
}

# =============================================================================
# PATTERN WEIGHTS (shared by both scanners)
# =============================================================================

PATTERN_WEIGHTS = {
    # Tier 1 - Highest weights
    'direct_override': 70,
    'role_manipulation': 120,
    'jailbreak_personas': 70,
    
    # Tier 2 - High severity
    'privilege_escalation': 100,
    'template_extraction': 60,
    'context_confusion': 35,
    'delimiter_injection': 35,
    'nested_injection': 35,
    'semantic_attack': 87,
    
    # Tier 3 - Orchestration attacks
    'compositional_attack': 80,
    
    # Critical but rare
    'secret_detection': 60,
    
    # New v2.1 categories
    'payload_delivery': 80,
    'multimodal_injection': 70,
    'rag_poisoning': 70,
    'session_persistence': 40,
    'agent_manipulation': 70,
    'delimiter_injection_advanced': 40,
    'unicode_evasion': 50,
    'whitespace_obfuscation': 30,
    
    # Deep scan only weights
    'obfuscation': 15,
    'data_exfiltration': 50,
    'history_leakage': 35,
    'link_injection': 15,
    'code_execution': 40,
    'unauthorized_access': 35,
    'xss_injection': 30,
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_patterns_for_scanner(scanner_type):
    """
    Get appropriate pattern dictionary for scanner.
    
    Args:
        scanner_type: 'quick' or 'deep'
    
    Returns:
        dict: Combined pattern dictionary
    """
    if scanner_type == 'quick':
        return SHARED_PATTERNS.copy()
    
    elif scanner_type == 'deep':
        # Merge shared + deep-only patterns
        patterns = SHARED_PATTERNS.copy()
        patterns.update(DEEP_SCAN_ONLY)
        return patterns
    
    else:
        raise ValueError(f"Unknown scanner type: {scanner_type}")

def get_weights():
    """Get pattern weights dictionary."""
    return PATTERN_WEIGHTS.copy()

# =============================================================================
# VERSION INFO
# =============================================================================

VERSION = "2.1"
LAST_UPDATED = "2025-11-23"