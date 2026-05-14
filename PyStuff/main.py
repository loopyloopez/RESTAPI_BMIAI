
    

import sys
from pathlib import Path

import torch
import torch.nn as nn
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

aiPath = Path(__file__).parent / "finalModel-2.pth"
if not aiPath.is_file():
    raise FileNotFoundError(f"Model file not found at {aiPath}")

class MakeModel(nn.Module):
    def __init__(self, hidden: int, num_classes: int, vocab_size: int, embed_dim: int):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.Net = nn.Sequential(
            nn.Flatten(),                        # [1152, 9, 32] → [1152, 288]
            nn.Linear(9 * embed_dim, hidden),    # 9 * 32 = 288
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.embedding(x)
        return self.Net(x)
    
    
M0 = MakeModel(hidden=32, vocab_size=29682, num_classes=1, embed_dim=32)
M0.load_state_dict(torch.load(aiPath, weights_only=True))


import time
import os

def BMI_Test(name:str, height:float, weight:float) -> str:
  nameT = TT([name])
 # print(f"name shape:{nameT.shape}, dataX shape:{dataX.shape}")
  M0.eval()
  with torch.inference_mode():
    y_logit_test = M0(nameT)
    y_prob_test = torch.sigmoid(y_logit_test)
    y_result = torch.round(y_prob_test)
  invert = {1:"FAT",0:"HEALTHY"}
  return invert[int(y_result)]

def TT(x) -> torch.Tensor:
    encoded = tokenizer(
        list(x),
        return_tensors="pt",
        padding="max_length",  # always pad to max_length
        truncation=True,
        max_length=9           # match your training seq length
    )
    return encoded["input_ids"]




def main(): 
    name = sys.argv[1]
    output = BMI_Test(name, 0, 0)
    print(output)

if __name__ == "__main__":
    main()