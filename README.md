A new optimisation technique for Open-Shop Scheduling
====

## Presentation

After a request from the French [Ecole Navale](https://www.ecole-navale.fr), I did a literature survey of known techniques and heuristics used in open-shop scheduling problems. Their goal was to generate and optimise automatically oral exam schedules according to arbitrary rules (namely, letting student rest a bit between each exam).

After developing a graph networks and simulated-annealing based method, and based on my partner Benjamin Rabdeau's genetic optimisation algorithms, I came up with a new hybrid heuristics: optimising genes with simulated annealing as a proxy for optimising the makespan of the actual schedule.

## Fonctionnement

In more formal terms, we want to optimise a schedule with

-   _n_ jobs that represent students;
-   _p_ machines that represent examiners.

Finding and optimising solutions to this problem can be done using the classic literature's graph representation of the problem and its constraints, but also using a chromosome-based representation of our solution. In the latter, we modelise a solution as *p +1* chromosomes. The first chromosome tells the affectation order for examiners, the *p* others represent the order used to assign students with each examiner.

For instance, the following gene:

```
123 1234 4231 2314
```

Translates to:

```
123  : schedules for the examiners will be created in order 1, 2, 3
1234 : for the first examiner, students will be chosen in the order 1, 2, 3, 4
4321 : for the first examiner, students will be chosen in the order 4, 3, 2, 1
2314 : for the first examiner, students will be chosen in the order 2, 3, 1, 4
```

The perturbation applied to the solution (used in the Metropolis algorithm) is the following:

```
123 12*34* 4231 2314
```

becomes

```
123 12*43* 4231 2314
```

*Stars represent what has been changed.*

## Appendix: code representation of the problem's objects

Since this optimisation routine is mainly used as a proof of concept, and to avoid the heaviness of object-oriented programming for a problem that simple, we use Python's primitive types.

For example, an examiner is represented by:

```py
examiner = {
    "Number" : 3,
    "Exams"  : {
        1 : 3,
        2 : 5,
        ...
        n : ...
    }
}
```

The number designates the length of the exam for this examiner (using `durations[examiner_number]` (`durations` is a globally defined list) as well as placing it on the schedule graph at the end.

A student can also be represented by a dictionary:

```
student = {
    1 : 0,
    2 : 3,
    ...
    p : 6
}
```

Students do not need to have an identification number (they are freely swappable), we simply use that dictionary to tell what time each exam is for this student, for each examiner.

Finally, storing examinations' durations and define the minimum time between two examinations, we use variables `durations` and `delay`

```py
durations = [
    2, # Examiner 1's examination duration is 2 time units
    3, # Examiner 2's examination duration is 3 time units
    ...
]

# A student needs a 1 time unit delay (at least) between two examinations
delay = 1
```

## Appendix: schedule-reconstruction algorithm

Materialising a schedule from a chromosome is done using a greedy algorithm, that works as explained here. 

The global problem is divided in *p* local (per examiner) makespan optimisation problems. We "fill" each examiner's schedule in the order given by the gene, in the order given by the corresponding gene (and globally, in the order of the first gene).

To do so, we read the examiner's gene and we attribute student examinations in the order it gives. To be sure the generated solution is consistent (two examiners should not be with a given student at the same time), we check, before assigning an examination time *t*, that both the student and the examiner are not "somewhere else" at time *t* (by checking all already assigned examiners' schedules).

## Questions and remarks

[Feel free to open an issue.](https://github.com/KowalskiThomas/OpenShopScheduling/issues/new)
