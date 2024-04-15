import numpy as np
import matplotlib.pyplot as plt

def create_student_data():
    num_majors = 3
    num_semesters = 2

    data = []
    for i in range(num_majors):
        major_data = []
        major_name = input(f"{i+1}. 전공명을 입력하세요(3개): ")  # 전공명 입력 받기
        major_data.append(major_name)
        semester_data = []
        for j in range(num_semesters):
            semester_data.append(float(input(f"{major_name}의 {j+1}학기 점수를 입력하세요: ")))
        major_data.extend(semester_data)
        data.append(major_data)

    arr1 = np.array(data)
    return arr1  # 데이터 반환

# 학생 데이터 생성
student_data = create_student_data()
print("Student Data:")
print(student_data)

# 전공명 추출
major_names = student_data[:, 0]

# 1학기와 2학기 점수 추출 및 숫자로 변환
semester1_scores = student_data[:, 1].astype(float)
semester2_scores = student_data[:, 2].astype(float)

# 1학기와 2학기 평균 계산
semester1_mean = np.mean(semester1_scores)
semester2_mean = np.mean(semester2_scores)

# 레이블 정의
labels = ['first semester', 'second semester']

# 평균을 막대 그래프로 나타내기
bar_width = 0.35
index = np.arange(len(labels))
plt.bar(index, [semester1_mean, semester2_mean], bar_width, label='the average score')
plt.xlabel('semester')
plt.ylabel('the average score')
plt.title('Comparing the average score for the 1st and 2nd semesters')
plt.xticks(index, labels)
plt.legend()
plt.show()
