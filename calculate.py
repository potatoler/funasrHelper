#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def remove_key_and_space(line:str, remove_space=True):
    """
    Remove the key at the beginning of a line.\\
    Of course you can also keep the sapces.
    """
    parts = line.strip().split(maxsplit=1)
    if len(parts) < 2:
        return ""
    text = parts[1]
    if remove_space:
        text = text.replace(" ", "")
    return text

def compare_lines(pred_line: str, tag_line:str):
    """
    Compare pred_line with tag_line.\\
    return (error_count, total_count)\\
    NOTE: if the lengths of two texts are different, the extra part is also counted as error.
    """
    pred_text = remove_key_and_space(pred_line, remove_space=False)
    tag_text = remove_key_and_space(tag_line, remove_space=True)
    
    maxlen = max(len(pred_text), len(tag_text))
    error_count = 0
    for i in range(maxlen):
        c1 = pred_text[i] if i < len(pred_text) else ""
        c2 = tag_text[i] if i < len(tag_text) else ""
        if c1 != c2:
            error_count += 1
    return error_count, maxlen

def colored(text, color_code):
    """
    Colour texts.
    """
    RESET = "\033[0m"
    return f"{color_code}{text}{RESET}"

def main():
    pred_filename = "path to your model's prediction file"
    tag_filename = "path to your evaluation text file"
    
    try:
        with open(pred_filename, encoding="utf-8") as f:
            pred_lines = f.readlines()
    except Exception as e:
        print(f"Error opening file {pred_filename}:{e}", file=sys.stderr)
        return

    try:
        with open(tag_filename, encoding="utf-8") as f:
            tag_lines = f.readlines()
    except Exception as e:
        print(f"Error opening file {tag_filename}:{e}", file=sys.stderr)
        return

    if len(pred_lines) != len(tag_lines):
        print("[WARNING] The number of lines in the two files is not equal!", file=sys.stderr)
    
    total_error_chars = 0
    total_characters = 0

    pure_count = 0
    far_count = 0
    lost_count = 0
    
    sample_categories = []

    for idx, (p_line, t_line) in enumerate(zip(pred_lines, tag_lines)):
        err, char_count = compare_lines(p_line, t_line)
        total_error_chars += err
        total_characters += char_count

        # New classification logic:
        # If the sample has no errors, classify as PURE
        # If there are errors, calculate error_rate = error_count / char_count
        # When error_rate <= 30%, classify as FAR
        # Otherwise classify as LOST

        if char_count == 0:
            # Consider this sample as PURE if there are no characters to compare
            sample_categories.append("PURE")
            pure_count += 1
        elif err == 0:
            sample_categories.append("PURE")
            pure_count += 1
        else:
            error_rate = err / char_count

            if error_rate <= 0.1:
                sample_categories.append("PURE")
                pure_count += 1
            elif error_rate <= 0.3:
                sample_categories.append("FAR")
                far_count += 1
            else:
                sample_categories.append("LOST")
                lost_count += 1

    if total_characters == 0:
        error_rate_total = 0
        correct_rate = 0
    else:
        error_rate_total = total_error_chars / total_characters
        correct_rate = (total_characters - total_error_chars) / total_characters

    # Set the TRACK title based on the sample categories
    total_samples = len(sample_categories)
    track_title = "TRACK COMPLETE"
    # ANSI color codes
    LIGHT_BLUE = "\033[94m"
    PURPLE = "\033[35m"
    RED = "\033[91m"

    # Title rules:
    # - PURE MEMORY if all PURE samples
    # - FULL RECALL if not all PURE, but no LOST
    # - TRACK LOST if LOST samples exceed 20%
    # - TRACK COMPLETE otherwise

    if total_samples > 0 and pure_count == total_samples:
        track_title = colored("PURE MEMORY", LIGHT_BLUE)
    elif lost_count == 0 and total_samples > pure_count:
        track_title = colored("FULL RECALL", PURPLE)
    elif total_samples > 0 and (lost_count / total_samples) > 0.2:
        track_title = colored("TRACK LOST", RED)
    else:
        track_title = "TRACK COMPLETE"

    print(f"\033[1m{track_title}\033[0m")
    
    PINK = "\033[95m"
    YELLOW = "\033[93m"

    print(colored(f"PURE: {pure_count}", PINK))
    print(colored(f"FAR: {far_count}", YELLOW))
    print(colored(f"LOST: {lost_count}", RED))
    
    # accuracy is calculated as (PURE + 0.5 * FAR) / TOTAL, the Arcaea way
    print(f"wer: {error_rate_total*100:.2f}%   acc: {(pure_count + far_count*0.5) / total_samples * 100:.2f}%")

if __name__ == '__main__':
    main()
