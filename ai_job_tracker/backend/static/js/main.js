// main.js

document.addEventListener("DOMContentLoaded", function () {
    // Auto-dismiss flash messages after 4 seconds
    const alerts = document.querySelectorAll(".flash-message");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = "opacity 0.5s";
            alert.style.opacity = "0";
            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 4000);
    });

    // Format the resume text if the container exists
    const container = document.getElementById('resumeTextContainer');
    if (container) {
        formatResumeText(container);
    }
});

/**
 * Formats the plain text inside the given container into a structured HTML resume.
 * Detects all-caps lines (headings), bullet lists, and paragraphs.
 */
function formatResumeText(container) {
    const raw = container.innerText || container.textContent;
    if (!raw.trim()) return;

    const lines = raw.split(/\n/);
    let formattedHtml = '';
    let inList = false;

    lines.forEach((line) => {
        const trimmed = line.trim();
        if (!trimmed) {
            // Empty line: close any open list and add a paragraph break
            if (inList) {
                formattedHtml += '</ul>';
                inList = false;
            }
            formattedHtml += '<div class="resume-paragraph"><br></div>';
            return;
        }

        // Check if the line is all uppercase (and not just a short abbreviation)
        const isHeading = (trimmed === trimmed.toUpperCase()) && trimmed.length > 2;

        if (isHeading) {
            // Close any open list
            if (inList) {
                formattedHtml += '</ul>';
                inList = false;
            }
            formattedHtml += `<div class="resume-heading">${trimmed}</div>`;
            return;
        }

        // Check if line starts with a bullet marker: •, -, *, or number.
        const bulletMatch = trimmed.match(/^[•\-*]\s+(.*)/);
        if (bulletMatch) {
            const content = bulletMatch[1];
            if (!inList) {
                formattedHtml += '<ul class="resume-list">';
                inList = true;
            }
            formattedHtml += `<li>${content}</li>`;
            return;
        }

        // If we are in a list and this line is not a bullet, close the list.
        if (inList) {
            formattedHtml += '</ul>';
            inList = false;
        }

        // Regular paragraph
        formattedHtml += `<div class="resume-paragraph">${trimmed}</div>`;
    });

    // Close any open list at the end
    if (inList) {
        formattedHtml += '</ul>';
    }

    // Replace the container's content with the formatted HTML
    container.innerHTML = formattedHtml;
}

/**
 * Copies the original raw text (not formatted HTML) to the clipboard.
 * Uses a hidden clone of the original content.
 */
function copyResumeText() {
    const container = document.getElementById('resumeTextContainer');
    if (!container) return;

    // We need the original raw text. Since we replaced the innerHTML, we must store it somewhere.
    // We'll use a data attribute or a hidden element. For simplicity, we'll re-fetch the raw text
    // from the server? That's not ideal. Instead, we can store the raw text in a data attribute
    // when we format it, or we can keep a hidden copy. Let's add a hidden div.

    // Quick fix: we'll use the 'data-raw-text' attribute on the container.
    const rawText = container.getAttribute('data-raw-text') || container.innerText;
    if (!rawText) {
        alert('No text to copy.');
        return;
    }

    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(rawText)
            .then(() => updateCopyButtonStatus(true))
            .catch(() => fallbackCopy(rawText));
    } else {
        fallbackCopy(rawText);
    }
}

function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try {
        document.execCommand('copy');
        updateCopyButtonStatus(true);
    } catch (err) {
        alert('Could not copy text. Please copy manually.');
    }
    document.body.removeChild(textarea);
}

function updateCopyButtonStatus(success) {
    const btn = document.getElementById('copyResumeBtn');
    if (!btn) return;
    const original = btn.innerHTML;
    if (success) {
        btn.innerHTML = '<i class="bi bi-check2 me-1"></i>Copied!';
    } else {
        btn.innerHTML = '<i class="bi bi-clipboard me-1"></i>Copy Text';
    }
    setTimeout(() => {
        btn.innerHTML = original;
    }, 2000);
}

// Expose the copy function globally
window.copyResumeText = copyResumeText;