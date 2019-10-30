from random import randint, random
from copy import deepcopy
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def build_schedule(solution, new_examiners, new_students):
    """
    Builds the schedules induced by `solution` using a greedy algorithm.
    `new_examiners` et `new_students` shall be dictionaries with empty records (which means they should all map to -1)
    *No side-effects are present in this function*
    """
    examiners = deepcopy(new_examiners)
    students = deepcopy(new_students)

    def student_is_available(target_student, target_time, target_duration):
        """
        Checks whether a student is available at a given time for a certain duration
        :param target_student: the student
        :param target_time: the time at which the student should be available
        :param target_duration: the duration during which the student should be available
        :return:
        """
        for exam, exam_time in target_student.items():
            if exam_time == -1:
                continue

            if target_time <= exam_time < target_time + target_duration + delay:
                return False
            elif exam_time <= target_time < exam_time + durations[exam] + delay:
                return False

        return True

    def examiner_is_available(target_examiner, target_time):
        """
        Checks whether an examiner is available at a given time for his exam's duration
        :param target_examiner: the examiner
        :param target_time: the duration during which the examiner should be available
        :return:
        """
        examiner_number, examiner_exams = target_examiner["Number"], target_examiner["Exams"]

        for _, exam_time in examiner_exams.items():
            if exam_time == -1:
                continue

            if target_time <= exam_time < target_time + durations[examiner_number]:
                return False
            elif exam_time <= target_time < exam_time + durations[examiner_number]:
                return False

        return True

    examiners_order, *students_orders = solution

    for j in examiners_order:
        all_set = False
        t = 0
        while not all_set:
            all_set = [examiners[j]["Exams"][i] != -1 for i in range(student_count)] == [True] * student_count
            placed = False
            for student in students_orders[j]:
                if examiners[j]["Exams"][student] != -1:
                    continue

                if student_is_available(students[student], t, durations[j]):
                    if examiner_is_available(examiners[j], t):
                        placed = True
                        students[student][j] = t
                        examiners[j]["Exams"][student] = t
                        break

            if not placed:
                t += 1
            else:
                t += durations[j]

    return examiners, students


def duration(examiners_data):
    """
    Computes the duration of a solution
    :param examiners_data: the examiners data for the solution
    :return: the makespan for this solution
    """
    max_end = 0
    for jury in examiners_data:
        examiner_number, exams = jury["Number"], jury["Exams"]
        for student_number, exam_time in exams.items():
            if exam_time + durations[examiner_number] > max_end:
                max_end = exam_time + durations[examiner_number]

    return max_end


def perturbation(solution):
    """
    Applies a perturbation on the given solution.
    To do this, a random chromosome is chosen and two of its alleles are swapped.
    Example: 123 1234 1234 1234 gives 123 1243 1234 1234
    :param solution: the solution to perturb
    :return: the perturbed solution
    Only one gene is changed, to keep the perturbation limited.
    """
    solution = deepcopy(solution)

    chosen_index = randint(0, len(solution) - 1)

    sub_sequence = solution[chosen_index]
    sub_index = randint(0, len(sub_sequence) - 2)
    sub_sequence[sub_index], sub_sequence[sub_index + 1] = sub_sequence[sub_index + 1], sub_sequence[sub_index]

    solution[chosen_index] = sub_sequence

    return solution


def metropolis_criterion(solution, solution_with_perturbation, temperature, constant):
    """
    Applies the Metropolis criterion using the given parameters
    :param solution: the current solution
    :param solution_with_perturbation: the perturbed solution
    :param temperature: the current temperature
    :param constant: the "Boltzmann constant"
    :return: the solution to keep
    """
    rand = random()

    schedule = build_schedule(solution, examiners, students)[0]
    schedule_with_perturbation = build_schedule(solution_with_perturbation, examiners, students)[0]

    delta_makespan = duration(schedule_with_perturbation) - duration(schedule)

    if delta_makespan <= 0:
        return solution_with_perturbation
    else:
        if rand < np.exp(-1 * delta_makespan / (constant * temperature)):
            return solution_with_perturbation
        else:
            return solution


def initial_solution():
    """
    Creates a naive solution in the form 1..p 1..n 1..n ... 1..n
    :return: a naive solution
    """
    solution = [[i for i in range(len(durations))]]

    for _ in range(len(durations)):
        solution += [[j for j in range(len(students))]]

    return solution


def display_schedule(schedule):
    """
    Displays the given schedule in a MatPlotLib window
    :param schedule: the schedule to display
    """

    def display_patches(patches_sequence, margin=8):
        """
        Displays a sequence of MatPlotLib patches in a MatPlotLib window
        :param patches_sequence: the patches to display
        :param margin:
        :return:
        """
        plt.rcdefaults()
        fig, ax = plt.subplots()
        for p in patches_sequence:
            ax.add_patch(p)
        max_machines = max(rect.get_y() for rect in patches_sequence) + 1
        max_jobs = max(rect.get_x() + margin for rect in patches_sequence)
        plt.axis([0, max_jobs, 0, max_machines])
        plt.show()

    patches = list()
    colors = ["black", "darksalmon", "DarkKhaki", "DarkViolet", "red", "blue", "green", "cyan", "magenta", "yellow",
              "black", "IndianRed", "Pink", "Lavender", "DarkOrange", "GreenYellow", "Teal", "SteelBlue",
              "MidnightBlue", "Maroon", "DimGray"]

    for i, prof in enumerate(schedule):
        prof = prof["Exams"]
        for eleve, heure in prof.items():
            rekt = mpatches.Rectangle((heure, i), durations[i], 1, color=colors[eleve], ec="black")
            patches.append(rekt)

    display_patches(patches)


def simulated_annealing(temperature=1000,
                        decrease_function=lambda x: x - 10,
                        constant=100):
    """
    Applies the simulated annealing algorithm to the problem
    :param temperature: the initial temperature
    :param decrease_function: the function used to decrease the temperature at each iteration
    :param constant: the "Boltzmann constant"
    """

    solution = initial_solution()
    while temperature > 10:
        new_solution = perturbation(solution)
        solution = metropolis_criterion(solution, new_solution, temperature, constant)
        temperature = decrease_function(temperature)

    edt = build_schedule(solution, examiners, students)[0]
    return edt


if __name__ == '__main__':
    durations = [
        1,
        2,
        3,
        4,
        5
    ]

    student_count = 4
    delay = 1

    students = [
        {
            i: -1
            for i in range(len(durations))
        }
        for j in range(student_count)
    ]

    examiners = [
        {
            "Number": j,
            "Exams": {
                i: -1
                for i in range(len(students))
            }
        }
        for j in range(len(durations))
    ]

    # The algorithm is applied several times to get better results
    iterations = 100
    best_duration = float('inf')
    best_schedule = None
    for _ in range(iterations):
        edt = simulated_annealing()
        if duration(edt) < best_duration:
            best_schedule = edt

    display_schedule(best_schedule)
